import csv
import subprocess
import itertools
import platform

from collections import OrderedDict

from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.forms.models import modelformset_factory
from django.db.models import Q, ObjectDoesNotExist
from django.db import OperationalError, transaction
from django.contrib.contenttypes.models import ContentType

from Results.models import *  # This is absolutely necessary for dynamic form loading
from ScenarioCreator.models import *  # This is absolutely necessary for dynamic form loading
from ScenarioCreator.forms import *  # This is absolutely necessary for dynamic form loading
from ADSMSettings.models import unsaved_changes
from ADSMSettings.utils import graceful_startup, file_list, handle_file_upload, workspace_path, adsm_executable_command
from ScenarioCreator.population_parser import lowercase_header
from ScenarioCreator.utils import convert_user_notes_to_unit_id
from ScenarioCreator.models import VaccinationRingRule, RelationalFunction, ProbabilityDensityFunction
from ScenarioCreator.exporter import *
from ScenarioCreator.importer import *
from ScenarioCreator import function_graphs
from matplotlib import pyplot as plt


# Useful descriptions of some of the model relations that affect how they are displayed in the views
from ScenarioCreator.utils import whole_scenario_validation

singletons = ['Scenario', 'Population', 'Disease', 'VaccinationGlobal', 'OutputSettings', "DestructionGlobal", "ControlMasterPlan"]
abstract_models = {
    'Function':
        [('RelationalFunction', RelationalFunction),
         ('ProbabilityDensityFunction', ProbabilityDensityFunction)],
    'DiseaseSpread':
        [('DirectSpread', DirectSpread),
         ('IndirectSpread', IndirectSpread),
         ('AirborneSpread', AirborneSpread)],
}

spread_types = {'DirectSpread': (DirectSpread, 'direct_contact_spread'),
                'IndirectSpread': (IndirectSpread, 'indirect_contact_spread'),
                'AirborneSpread': (AirborneSpread, 'airborne_spread')}

def spaces_for_camel_case(text):
    return re.sub(r'([a-z])([A-Z])', r'\1 \2', text)


def add_breadcrumb_context(context, model_name, primary_key=None):
    context['pretty_name'] = spaces_for_camel_case(promote_to_abstract_parent(model_name))
    if model_name not in singletons:
        context['model_link'] = '/setup/' + model_name + '/'
        if primary_key is not None:
            context['model_link'] += primary_key + '/'
    else:  # for singletons, don't list the specific name, just the type
        context['title'] = 'Edit the ' + spaces_for_camel_case(model_name)


def population_panel_only(request):
    """#707 Fix by loading the production group section dynamically
    When creating new Production Type Groups, the population panel needs to be loaded asynchronously, but
    the contents depends on the context processor, which is normally only run on non-ajax requests.  This function
    collects the context in Ajax calls"""
    context = {'ProductionGroups': ProductionGroup.objects.all()}
    return render(request, 'population_panel.html', context)


def production_type_list_json(request):
    msg = list(ProductionType.objects.values_list('name', 'id'))
    return JsonResponse(msg, safe=False)  # necessary to serialize a list object


def jsonify(string_list):
    """Returns the name of the specific assignment or None"""
    if string_list:
        return string_list[0]
    else:
        return None


def population_panel_status_json(request):
    response = []

    for pt in ProductionType.objects.all():
        response.append({'name': pt.name,
                         'pk': pt.id,
                         'unit_count': Unit.objects.filter(production_type=pt).count(),
                         'spread': DiseaseSpreadAssignment.objects.filter(destination_production_type=pt).filter(
                             Q(direct_contact_spread__isnull=False,) |
                             Q(indirect_contact_spread__isnull=False) |
                             Q(airborne_spread__isnull=False)).count(),
                         'control': jsonify(ProtocolAssignment.objects.filter(control_protocol__isnull=False, production_type=pt).values_list('control_protocol__name', flat=True)),
                         'progression': jsonify(DiseaseProgressionAssignment.objects.filter(progression__isnull=False, production_type=pt).values_list('progression__name', flat=True)),
                         'zone': jsonify(ZoneEffectAssignment.objects.filter(effect__isnull=False, production_type=pt).values_list('zone__name', flat=True)),
                         })

    return JsonResponse(response, safe=False)


def spread_options_json(request):  # list of DiseaseSpreads by Type
    options = {
        'DirectSpread': {d.id: {'name': d.name, 'pk': d.id} for d in DirectSpread.objects.all()},
        'IndirectSpread': {d.id: {'name': d.name, 'pk': d.id} for d in IndirectSpread.objects.all()},
        'AirborneSpread': {d.id: {'name': d.name, 'pk': d.id} for d in AirborneSpread.objects.all()}
    }
    return JsonResponse(options)


def spread_inputs_json(request):
    options = {}
    for class_name, meta in spread_types.items():
        model, field_name = meta
        options[class_name] = {}
        for spread in model.objects.all():
            inputs = []
            for source in ProductionType.objects.all():
                query = DiseaseSpreadAssignment.objects.filter(**{'source_production_type': source, field_name: spread})
                if query.exists():
                    one_source = {'source': source.id,
                                  'destinations': [pair.destination_production_type.id for pair in query]}
                    inputs.append(one_source)

            options[class_name][spread.id] = inputs
    return JsonResponse(options)


def modify_spread_assignments(request):
    """
    called when a request to change the spread assignements is made. This function is called for all three spread assignment types
    :param request:
    :return: json summary of the request
    """
    # destinations is a list of integer ids
    destinations = [int(x) for x in request.POST.getlist('destinations[]')]
    # if a non-blank selection was made
    if 'destinations[]' in request.POST.keys() and request.POST['source']:  # when a user selects ----- there's no PK at all
        data = request.POST.dict()
        # if a spread assignment is being CREATED
        if 'POST' == data['action']:
            # for each destination
            for destination_pk in destinations:
                assignment = DiseaseSpreadAssignment.objects.filter(**{'source_production_type_id': int(data['source']),
                                                                       'destination_production_type_id': int(destination_pk)})
                parameter_class, field = spread_types[data['spread_type']]
                assignment.update(**{field: parameter_class.objects.get(id=int(data['pk']))})  # saves immediately
                # Debug output:
                source = ProductionType.objects.get(id= int(data['source'])).name
                destination = ProductionType.objects.get(id=int(destination_pk)).name
                print("ADD", field, "SOURCE:", source, "DESTINATION:", destination)

        # if a spread assignment is being DELETED
        if 'DELETE' == data['action']:  # Django doesn't allow you to parametrize DELETE http_method
            # for each destination
            for destination_pk in destinations:
                assignment = DiseaseSpreadAssignment.objects.filter(**{'source_production_type_id': int(data['source']),
                                                                       'destination_production_type_id': int(destination_pk)})
                parameter_class, field = spread_types[data['spread_type']]
                assignment.update(**{field: None})  # saves immediately
                # Debug output:
                source = ProductionType.objects.get(id= int(data['source'])).name
                destination = ProductionType.objects.get(id=int(destination_pk)).name
                print("DEL", field, "SOURCE:", source, "DESTINATION:", destination)

    return spread_inputs_json(request)


def disease_spread_assignments_json(request):
    source_rows = {}
    for source in ProductionType.objects.all().order_by('name'):
        one_row = {'name': source.name, 'pk': source.id, 'destinations': {}}
        for destination in ProductionType.objects.all().order_by('name'):
            assignment = {'name': destination.name, 'pk': destination.id, 'DirectSpread': None, 'IndirectSpread': None,
                          'AirborneSpread': None}
            query = DiseaseSpreadAssignment.objects.filter(source_production_type=source,
                                                           destination_production_type=destination)
            if query.exists():
                assignment['DirectSpread'] = query.first().direct_contact_spread_id
                assignment['IndirectSpread'] = query.first().indirect_contact_spread_id
                assignment['AirborneSpread'] = query.first().airborne_spread_id
            one_row['destinations'][destination.name] = assignment
        source_rows[source.name] = one_row
    return JsonResponse(source_rows, safe=False)


def disable_all_controls_json(request):
    if 'POST' in request.method:
        new_value = request.POST['use_controls']
        set_to = new_value == 'false'  # logical inversion because of use_controls vs disable_controls
        controls = VaccinationGlobal.objects.get()
        controls.disable_all_controls = set_to
        controls.save()
        return JsonResponse({'status': 'success'})
    else:
        return JsonResponse({'disable_all_controls': VaccinationGlobal.objects.get().disable_all_controls})
    

def initialize_spread_assignments():
    pts = list(ProductionType.objects.all())
    for source in pts:
        for destination in pts:
            DiseaseSpreadAssignment.objects.get_or_create(
                source_production_type=source,
                destination_production_type=destination)
        

def assign_disease_spread(request):
    initialize_spread_assignments()

    context = {'base_page': 'ScenarioCreator/AssignSpread.html'}
    return render(request, 'ScenarioCreator/MainPanel.html', context)


def zone_effects(request):
    ZoneEffectAssignment.objects.ensure_all_zones_and_production_types()
    assignment_form_set = modelformset_factory(ZoneEffectAssignment, form=ZoneEffectAssignmentForm, extra=0)

    context = {'title': 'What Effect does a Zone have on each Production Type?'}
    if save_formset_succeeded(assignment_form_set, ZoneEffectAssignment, context, request):
        return redirect(request.path)
    else:
        forms = assignment_form_set(queryset=ZoneEffectAssignment.objects.all())
        forms_sorted_by_pt = sorted(forms, key=lambda x: x.instance.production_type.name)
        forms_grouped_by_pt = itertools.groupby(forms_sorted_by_pt, lambda x: x.instance.production_type)

        context['formset'] = assignment_form_set
        context['formset_headings'] = Zone.objects.order_by('id')
        context['formset_grouped'] = {k: sorted(v, key=lambda x: x.instance.zone.id) 
                                        for k,v in forms_grouped_by_pt}
        context['base_page'] = 'ScenarioCreator/FormSet2D.html'

        return render(request, 'ScenarioCreator/MainPanel.html', context)


def save_formset_succeeded(MyFormSet, TargetModel, context, request):
    try:
        initialized_formset = MyFormSet(request.POST, request.FILES, queryset=TargetModel.objects.all())
        if initialized_formset.is_valid():
            instances = initialized_formset.save()
            context['formset'] = initialized_formset
            return True
        return False
    except ValidationError:
        return False


def populate_forms_matching_ProductionType(MyFormSet, TargetModel, context, missing, request, template='ScenarioCreator/3Panels.html',
                                           html='ScenarioCreator/AssignmentList.html'):
    """FormSet is pre-populated with existing assignments and it detects and fills in missing
    assignments with a blank form with production type filled in."""
    if save_formset_succeeded(MyFormSet, TargetModel, context, request):
        return redirect(request.path)
    else:
        forms = MyFormSet(queryset=TargetModel.objects.all())
        for index, pt in enumerate(missing):
            index += TargetModel.objects.count()
            forms[index].fields['production_type'].initial = pt.id
        context['formset'] = forms
        context['base_page'] = html
        return render(request, template, context)


def assign_protocols(request):
    missing = ProductionType.objects.filter(protocolassignment__isnull=True)
    ProtocolSet = modelformset_factory(ProtocolAssignment, extra=len(missing), form=ProtocolAssignmentForm)
    context = {'title': 'Assign a Control Protocol to each Production Type'}
    return populate_forms_matching_ProductionType(ProtocolSet, ProtocolAssignment, context, missing, request,
                                                  template='ScenarioCreator/MainPanel.html',
                                                  html='ScenarioCreator/FormSet.html')


def assign_progressions(request):
    """FormSet is pre-populated with existing assignments and it detects and fills in missing
    assignments with a blank form with production type filled in."""
    initialize_spread_assignments()
    missing = ProductionType.objects.filter(diseaseprogressionassignment__isnull=True)
    ProgressionSet = modelformset_factory(DiseaseProgressionAssignment,
                                          extra=len(missing),
                                          form=DiseaseProgressionAssignmentForm)
    context = {'title': 'Assign Disease Progressions'}
    return populate_forms_matching_ProductionType(ProgressionSet, DiseaseProgressionAssignment, context, missing, request,
                                                  template='ScenarioCreator/MainPanel.html')


def protocols_json(request):
    data = []
    for protocol in ControlProtocol.objects.all():
        entry = {'name': str(protocol.name),
                 'pk': protocol.id,
                 'tabs': [
                     {'name':'Detection', 'can_select': True, 'enabled':bool(protocol.use_detection), 'field':'use_detection', 'valid': protocol.tab_is_valid('use_detection')},
                     {'name':'Tracing', 'can_select': True, 'enabled':bool(protocol.use_tracing), 'field':'use_tracing', 'valid': protocol.tab_is_valid('use_tracing')},
                     {'name':'Testing', 'can_select': True, 'enabled':bool(protocol.use_testing), 'field':'use_testing', 'valid': protocol.tab_is_valid('use_testing')},
                     {'name':'Exams', 'can_select': True, 'enabled':bool(protocol.use_exams), 'field':'use_exams', 'valid': protocol.tab_is_valid('use_exams')},
                     {'name':'Destruction', 'can_select': True, 'enabled':bool(protocol.use_destruction), 'field':'use_destruction', 'valid': protocol.tab_is_valid(
                         'use_destruction')},
                     {'name':'Vaccination', 'can_select': False, 'enabled':bool(vaccination_trigger_in_use(protocol)), 'field':'use_vaccination', 'valid': protocol.tab_is_valid(
                         'use_vaccination')},
                     {'name':'Cost Accounting', 'can_select': True, 'enabled':bool(protocol.use_cost_accounting), 'field':'use_cost_accounting', 'valid': protocol.tab_is_valid(
                         'use_cost_accounting')},
                     ]}
        data.append(entry)
    return JsonResponse(data, safe=False)


def update_protocol_enabled(request, primary_key, field):
    """Does nothing but save the `field` value to the database.  Ex: use_detection use_tracing use_destruction
    use_vaccination use_exams use_testing use_cost_accounting"""
    #data = json.loads(request.POST.content.decode())
    value = request.POST.get('value') == 'true'  #False otherwise
    ControlProtocol.objects.filter(id=int(primary_key)).update(**{field: value})  # specifically the value of field, not the word 'field'
    return JsonResponse({})

def collect_backlinks(model_instance):
    """:param model_instance: Django Model Instance
    :return: A dict of Models that reference the current
    Useful for determining if an instance can be deleted.  Includes hyperlinks to the related models
    """
    from django.contrib.admin.utils import NestedObjects
    collector = NestedObjects(using='scenario_db')  # or specific database
    collector.collect([model_instance])  # https://docs.djangoproject.com/en/1.7/releases/1.7/#remove-and-clear-methods-of-related-managers
    dependants = collector.nested()  # fun fact: spelling differs between America and Brittain
    #print("Found related models:", dependants)
    links = {}
    if len(dependants[1:]):
        for direct_reference in dependants[1:][0]:  # only iterates over the top level
            if not isinstance(direct_reference, list) and not isinstance(direct_reference, RelationalPoint):  # Points are obvious, don't include them
                name = direct_reference.__class__.__name__
                try:  # not everything has a name attr
                    links[str(direct_reference)] = '/setup/%s/%i/' % (name, direct_reference.pk)
                except:
                    links['%s:%i' % (name, direct_reference.pk)] = '/setup/%s/%i/' % (name, direct_reference.pk)
    #print(links)
    return links


def initialize_relational_form(context, primary_key, request):
    if not primary_key or primary_key == 'new':
        model = RelationalFunction()
        main_form = RelationalFunctionForm(request.POST or None)
    else:
        model = RelationalFunction.objects.get(id=primary_key)
        main_form = RelationalFunctionForm(request.POST or None, instance=model)
        context['model_link'] = '/setup/RelationalFunction/' + primary_key + '/'
        context['backlinks'] = collect_backlinks(model)
        context['deletable'] = context['model_link'] + 'delete/'
    context['form'] = main_form
    context['model'] = model
    return context

def export_functions(request, block):
    '''
    "Functions" as in relational functions and probability density functions.

    Exports to a single file, delimited by "REL_" for relational functions and "PDF_" for probability density functions.
    Files are saved in the same folder as the .db for each scenario. Exporting the same scenario multiple times overwrites
    the existing file.
    :param block: "rel" or "pdf" to determine which export to run.
    :return: Redirect to the scenario description.
    '''
    if block == "rel":
        # get the relational function model
        relfunction_model = globals()["RelationalFunction"]
        # get all of the relational functions
        relfunction_objects = relfunction_model.objects.all()
        # get the relational function points model
        relpoints_model = globals()["RelationalPoint"]
        # get all of the relational points
        relpoints_objects = relpoints_model.objects.all()
        # export the relational functions, export_relational_functions() is located in exporter.py
        export_relational_functions(relfunction_objects, relpoints_objects)
        pass
    elif block == "pdf":
        # get the pdf model
        pdf_model = globals()["ProbabilityDensityFunction"]
        # get all of the pdfs
        pdf_objects = pdf_model.objects.all()
        # export the pdfs, export_pdfs() is located in exporter.py
        export_pdfs(pdf_objects)
    return redirect("/setup/Scenario/1/")

def import_functions(request, block):
    '''
    "Functions" as in relational functions and probability density functions.

    Imports from all files located in the same location as the .db for each scenario that are delimited by "PDF_" for
    Probability Density Functions or "REL_" for relational functions. Will not import functions from files that include
    the current scenarios name.

    :param block: "rel" or "pdf" to determine which export to run.
    :return: Redirect to the scenario description.
    '''
    if block == "rel":
        # get the relational function model
        relfunction_model = globals()["RelationalFunction"]
        # get all the existing relational functions
        relfunction_objects = relfunction_model.objects.all()
        # import new relational functions, import_relational_functions() is located in importer.py
        import_relational_functions(relfunction_objects)
    elif block == "pdf":
        # get the pdf model
        pdf_model = globals()["ProbabilityDensityFunction"]
        # get all of the existing pdfs
        pdf_objects = pdf_model.objects.all()
        # import new pdfs, import_pdfs() is located in importer.py
        import_pdfs(pdf_objects)
    return redirect("/setup/Scenario/1/")

def deepcopy_points(request, primary_key, created_instance):
    queryset = RelationalPoint.objects.filter(relational_function_id=primary_key)
    for point in queryset:  # iterating over points already in DB
        point = RelationalPoint(relational_function=created_instance, x=point.x, y=point.y) # copy with new parent
        point.save()  # This assumes that things in the database are already valid, so doesn't call is_valid()
    queryset = RelationalPoint.objects.filter(relational_function_id=created_instance.id)
    formset = PointFormSet(queryset=queryset) # this queryset does not include anything the user typed in, during the copy operation
    # formset = PointFormSet(request.POST or None, instance=created_instance)
    return formset


def initialize_points_from_csv(request):
    """ Uses a file upload to create a series of points and add them to the request
    :param request: request that contains the file upload
    :return: request with initial_values set
    """
    file_path = handle_file_upload(request, is_temp_file=True, overwrite_ok=True)
    with open(file_path) as csvfile:
        dialect = csv.Sniffer().sniff(csvfile.read(1024))  # is this necessary?
        csvfile.seek(0)
        header = csv.Sniffer().has_header(csvfile.read(1024))
        csvfile.seek(0)
        if header:
            header = None  #DictReader will pull it off the first line
        else:
            header = ['x', 'y']
        reader = csv.DictReader(lowercase_header(csvfile), fieldnames=header, dialect=dialect)
        entries = [line for line in reader]  # ordered list
        try:
            (float(entries[0]['x']), float(entries[0]['y']))  # the header sneaks in when there's a mix of float and int
        except ValueError:
            entries = entries[1:]  # clip the header
        
        initial_values = {}
        for index, point in enumerate(entries):
            initial_values['relationalpoint_set-%i-id' % index] = ''
            initial_values['relationalpoint_set-%i-relational_function' % index] = ''
            initial_values['relationalpoint_set-%i-x' % index] = point['x'].strip()
            initial_values['relationalpoint_set-%i-y' % index] = point['y'].strip()
            initial_values['relationalpoint_set-%i-DELETE' % index] = ''  # these could be set to delete by the js
        initial_values['relationalpoint_set-TOTAL_FORMS'] = str(len(entries))
        initial_values['relationalpoint_set-INITIAL_FORMS'] = '0'
        initial_values['relationalpoint_set-MAX_NUM_FORMS'] = '1000'
        request.POST.update(initial_values)
    return request


def relational_function(request, primary_key=None, doCopy=False):
    """This handles the edge case of saving, copying, and creating Relational Functions.  RFs are different from any
    other model in ADSM in that they have a list of RelationalPoints.  These points are listed alongside the normal form.
    Rendering this page means render a form, then a formset of points.  Saving is more complex because the points also
    foreignkey back to the RelationalFunction which must be created before it can be referenced.

    It is possible to integrate this code back into the standard new / edit / copy views by checking for
    context['formset'].  The extra logic for formsets could be kicked in only when one or more formsets are present. At
    the moment integration looks like a bad idea because it would mangle the happy path for the sake of one edge case.
    :param request:
    :param primary_key: None or a number if editing
    :param doCopy: copying will clear old primary keys so django will create new entries"""
    context = initialize_relational_form({}, primary_key, request)
    context['action'] = request.path
    if 'file' in request.FILES:  # data file is present
        request = initialize_points_from_csv(request)
    if context['form'].is_valid():
        created_instance = None
        if doCopy:
            created_instance = context['form'].instance
            created_instance.pk = None  # This will cause a new instance to be created
            created_instance.save()
            context['formset'] = PointFormSet(request.POST or None, instance=created_instance)
        else:
            created_instance = context['form'].instance
            created_instance.save()
            context['formset'] = PointFormSet(request.POST or None, instance=created_instance)

        context['action'] = '/setup/RelationalFunction/%i/' % created_instance.id

        if created_instance:
            if context['formset'].is_valid():  # We need to run this to ensure that the data in the formset is populated
                pass
            if doCopy:
                # If the user clicked the +f() Variant button, then all of the rows that have data filled in will count
                # as changed. The points started as exact copies of the points from another relational function, so we
                # need to (1) erase their primary keys so they count as new objects, and (2) make this new relational
                # function their parent.
                for point in context['formset'].forms:
                    if point.changed_data:
                        point.instance.pk = None
                        point.instance.relational_function = created_instance
                        point.instance.save()
            else:
                # If the user clicked the Overwrite button, all we want is a delete() on any points for which the
                # Delete checkbox was checked, and a save() on any points that have changed.
                for point in context['formset'].forms:
                    if point.changed_data:
                        if point.cleaned_data['DELETE']:
                            point.instance.delete()
                        else:
                            point.instance.save()
        return HttpResponseRedirect(context['action'])
    else:
        context['formset'] = PointFormSet(request.POST or None, instance=context['model'])

    context['title'] = "Create a Relational Function"
    add_breadcrumb_context(context, "RelationalFunction")
    return render(request, 'ScenarioCreator/RelationalFunction.html', context)


def save_new_instance(initialized_form, request, context):
    model_instance = initialized_form.save()  # write to database
    model_name = model_instance.__class__.__name__
    context['model_name'] = model_name
    if model_name in singletons:  #they could have their own special page: e.g. Population
        return redirect('/setup/%s/1/' % model_name)
    if request.is_ajax():
        return HttpResponseRedirect('/setup/%s/%s' % (model_name, model_instance.id))
    return render(request, 'ScenarioCreator/crispy-model-form.html', context)


def new_form(request, initialized_form, context):
    if initialized_form.is_valid():
        model_instance = initialized_form.save()  # write to database
        link = context['action'].split('/')
        context['action'] = '/' + '/'.join([link[1], link[2], str(model_instance.id)]) + '/'  # not new if it has an id 
    model_name, model = get_model_name_and_model(request)
    context['model_name'] = model_name
    if model_name in singletons:  # they could have their own special page: e.g. Population
        context['base_page'] = 'ScenarioCreator/Crispy-Singleton-Form.html'
        # #422 Singleton models now load in a fragment to be refreshed the same way that other forms
        #  are loaded dynamically
        return render(request, 'ScenarioCreator/MainPanel.html', context)
    if model_name == 'ProbabilityDensityFunction':
        return render(request, 'ScenarioCreator/ProbabilityDensityFunctionForm.html', context)
    return render(request, 'ScenarioCreator/crispy-model-form.html', context)  # render in validation error messages


def get_model_name_and_form(request):
    model_name = re.split('\W+', request.path)[2]  # Second word in the URL
    form = globals()[model_name + 'Form']  # IMPORTANT: depends on naming convention
    return model_name, form


def get_model_name_and_model(request):
    """A slight variation on get_mode_name_and_form useful for cases where you don't want a form"""
    model_name = re.split('\W+', request.path)[2]  # Second word in the URL
    model = globals()[model_name]  # IMPORTANT: depends on import *
    return model_name, model


def initialize_from_existing_model(primary_key, request):
    """Raises an ObjectDoesNotExist exception when the primary_key is invalid"""
    model_name, form_class = get_model_name_and_form(request)
    model = form_class.Meta.model.objects.get(id=primary_key)  # may raise an exception
    initialized_form = form_class(request.POST or None, instance=model)
    return initialized_form, model_name


'''New / Edit / Copy / Delete / List that are called from model generated URLs'''
def new_entry(request, second_try=False):
    try:
        model_name, form = get_model_name_and_form(request)
        model_name, model = get_model_name_and_model(request)
        if model_name == 'RelationalFunction':
            return relational_function(request)
        if model_name in singletons and model.objects.count():
            return edit_entry(request, 1)
        initialized_form = form(request.POST or None)
        context = {'form': initialized_form,
                   'title': "Create a new " + spaces_for_camel_case(model_name),
                   'action': request.path,
                   'new_form': True}
        add_breadcrumb_context(context, model_name)
        return new_form(request, initialized_form, context)
    except OperationalError:
        if not second_try:
            graceful_startup()
            return new_entry(request, True)
        return new_form(request, initialized_form, context)


def edit_entry(request, primary_key):
    model_name, form = get_model_name_and_form(request)
    if model_name == 'RelationalFunction':
        return relational_function(request, primary_key)

    try:
        initialized_form, model_name = initialize_from_existing_model(primary_key, request)
    except (ObjectDoesNotExist, OperationalError):
        request.path = '/setup/%s/new/' % model_name
        return new_entry(request)
    context = {'form': initialized_form,
               'title': str(initialized_form.instance),
               'action': request.path}
    add_breadcrumb_context(context, model_name, primary_key)

    if model_name == 'ProbabilityDensityFunction':
        context['backlinks'] = collect_backlinks(initialized_form.instance)
        context['deletable'] = '/setup/ProbabilityDensityFunction/%s/delete/' % primary_key

    if hasattr(initialized_form, 'soft_clean'):
        initialized_form.soft_clean(request.method)

    return new_form(request, initialized_form, context)


def copy_entry(request, primary_key):
    model_name, form = get_model_name_and_form(request)
    if model_name == 'RelationalFunction':
        return relational_function(request, primary_key, doCopy=True)
    try:
        initialized_form, model_name = initialize_from_existing_model(primary_key, request)
        if 'name' in initialized_form:
            initialized_form.initial['name'] += " - Copy"
    except ObjectDoesNotExist:
        return redirect('/setup/%s/new/' % model_name)
    context = {'form': initialized_form, 
               'title': "Copy a " + spaces_for_camel_case(model_name), 
               'action': request.path, 
               'model_name': model_name}
    if initialized_form.is_valid() and request.method == 'POST':
        initialized_form.instance.pk = None  # This will cause a new instance to be created
        return save_new_instance(initialized_form, request, context)
    return render(request, 'ScenarioCreator/crispy-model-form.html', context)


def delete_entry(request, primary_key):
    model_name, model = get_model_name_and_model(request)
    model.objects.get(pk=primary_key).delete()
    unsaved_changes(True)
    if model_name not in singletons:
        return redirect('/setup/%s/' % model_name)  # model list
    else:
        if model_name == "Population":
            print("Deleting Population Dependant Models.")

            try:
                VaccinationRingRuleModel = globals()["VaccinationRingRule"]
                VaccinationRingRuleModel.objects.get(pk=1).delete()
            except VaccinationRingRule.DoesNotExist:
                pass

            try:
                VaccinationGlobalModel = globals()["VaccinationGlobal"]
                VaccinationGlobalModel.objects.get(pk=1).delete()
            except VaccinationGlobal.DoesNotExist:
                pass

            try:
                DiseaseDetectionModel = globals()["DiseaseDetection"]
                DiseaseDetectionObjects = DiseaseDetectionModel.objects.all()
                for DiseaseDetectionObject in DiseaseDetectionObjects:
                    DiseaseDetectionObject.delete()
            except DiseaseDetection.DoesNotExist:
                pass

            try:
                StopVaccinationModel = globals()["StopVaccination"]
                StopVaccinationObjects = StopVaccinationModel.objects.all()
                for StopVaccinationObject in StopVaccinationObjects:
                    StopVaccination.delete()
            except StopVaccination.DoesNotExist:
                pass

            print("Population Deletion Complete. Redirecting...")
        return redirect('/setup/%s/new/' % model_name)  # Population can be deleted, maybe others


def promote_to_abstract_parent(model_name):
    for key, value in abstract_models.items():  # fix for child models (DirectSpread, RelationalFunction) returning to the wrong place
        if model_name in [x[0] for x in value]:
            model_name = key
    return model_name


def trigger_list(request):
    layout = {
         'Start Triggers':
             [DiseaseDetection,
              RateOfNewDetections,
              DisseminationRate,
              SpreadBetweenGroups,
              TimeFromFirstDetection,
              DestructionWaitTime],
         'Stop Triggers':
             [StopVaccination],
         'Restart Triggers':  #Duplicate list from above because of filtering
             [DiseaseDetection,
              RateOfNewDetections,
              DisseminationRate,
              SpreadBetweenGroups,
              TimeFromFirstDetection,
              DestructionWaitTime],
    }
    context = {'title': "Vaccination Triggers", 
               'base_page': 'ScenarioCreator/VaccinationTriggerList.html',
               'categories': [{'name':'Start Triggers',
                               'models':[filtered_list_per_model(x, False) for x in layout['Start Triggers']]
                              }, 
                              {'name':'Stop Triggers',
                               'models':[list_per_model(x) for x in layout['Stop Triggers']]
                              },
                              {'name':'Restart Triggers',  # This exact name is used in the template VaccinationTriggerList.html
                               'models':[filtered_list_per_model(x, True) for x in layout['Restart Triggers']]
                              }
                          ]
               }
    
    return context


def vaccination_trigger_in_use(protocol):
    vaccination_triggers = trigger_list({})

    for category in vaccination_triggers['categories']:
        if category['name'] == "Start Triggers":
            for model in category['models']:
                if model['entries'] and len(model['entries']) > 0:
                    if not protocol.use_vaccination:
                        protocol.use_vaccination = True
                        protocol.save()
                    return True

    if protocol.use_vaccination:
        protocol.use_vaccination = False
        protocol.save()
    return False


def filtered_list_per_model(model_class, restart_trigger):
    model_name = model_class.__name__
    context = {'entries': model_class.objects.filter(restart_only=restart_trigger),
               'class': model_name,
               'name': spaces_for_camel_case(model_name)}
    return context



def list_per_model(model_class):
    model_name = model_class.__name__
    context = {'entries': model_class.objects.all(),
               'class': model_name,
               'name': spaces_for_camel_case(model_name),
               'wiki_link': getattr(model_class, 'wiki_link', None)}
    return context

def functions_panel(request, form=None):
    """Panel on the right that lists both Relational and Probability Functions with a graphic depiction"""
    context = {'models': [],
               'load_target': '#current-function',
               }
    if form is not None:
        context['form'] = form
    for local_name, local_model in abstract_models['Function']:
        context['models'].append(list_per_model(local_model))
    return render(request, 'functions_panel.html', context)  # no 3 panel layout

def export_relational_graph(request):

    # get the graph src, this looks a lot like a url. This is only used to extract the private key of the graph from
    graph_src = str(request.GET.get('graph_src', None))
    # extract said private key. This is used as a unique identifier for each function
    graph_pk = int(''.join(char for char in graph_src if char.isdigit()))

    # get the object itself. This will actually only be used to get the exact name of the function
    rel_graph = ScenarioCreator.models.RelationalFunction.objects.get(pk=graph_pk)

    # get the graph object, this comes back as an HttpResponse, but the image is in HttpResponse.content as bytes
    graph = function_graphs.existing_relational_graph(graph_pk)

    # ensure that the path will exist
    if not os.path.exists(workspace_path(scenario_filename() + "/Supplemental Output Files")):
        os.mkdir(workspace_path(scenario_filename() + "/Supplemental Output Files"))
    if not os.path.exists(workspace_path(scenario_filename() + "/Supplemental Output Files/Relational Function Graphs")):
        os.mkdir(workspace_path(scenario_filename() + "/Supplemental Output Files/Relational Function Graphs"))

    # write the image to file.
    with open(workspace_path(scenario_filename() + "/Supplemental Output Files/Relational Function Graphs/" + rel_graph.name + ".png"), "wb") as image_file:
        image_file.write(graph.content)

    # blank response - nothing happens on the front end.
    return JsonResponse({})

def export_pdf_graph(request):

    # get the graph src, this looks a lot like a url. This is only used to extract the private key of the graph from
    graph_src = str(request.GET.get('graph_src', None))
    # extract said private key. This is used as a unique identifier for each function
    graph_pk = int(''.join(char for char in graph_src if char.isdigit()))

    # get the object itself. This will actually only be used to get the exact name of the function
    pdf_graph = ScenarioCreator.models.ProbabilityDensityFunction.objects.get(pk=graph_pk)

    # get the graph object, this comes back as an HttpResponse, but the image is in HttpResponse.content as bytes
    graph = function_graphs.existing_probability_graph(graph_pk)

    # ensure that the path will exist
    if not os.path.exists(workspace_path(scenario_filename() + "/Supplemental Output Files")):
        os.mkdir(workspace_path(scenario_filename() + "/Supplemental Output Files"))
    if not os.path.exists(workspace_path(scenario_filename() + "/Supplemental Output Files/PDF Graphs")):
        os.mkdir(workspace_path(scenario_filename() + "/Supplemental Output Files/PDF Graphs"))

    # write the image to file
    with open(workspace_path(scenario_filename() + "/Supplemental Output Files/PDF Graphs/" + pdf_graph.name + ".png"), "wb") as image_file:
        image_file.write(graph.content)

    # blank response - nothing happens on the front end.
    return JsonResponse({})

def control_protocol_list(request):
    return model_list(request, 'ScenarioCreator/ControlProtocolList.html')


def model_list(request, base_page='ScenarioCreator/ModelList.html'):
    model_name, model = get_model_name_and_model(request)
    model_name = promote_to_abstract_parent(model_name)
    if model_name in 'Function RelationalFunction ProbabilityDensityFunction'.split():
        return functions_panel(request)
    if model_name == 'VaccinationTrigger':  # special case
        context = trigger_list(request)
    else:
        context = {'title': "Create " + spaces_for_camel_case(model_name) + "s",
                   'base_page': base_page,
                   'models': []}
        if model_name in abstract_models.keys():
            for local_name, local_model in abstract_models[model_name]:
                context['models'].append(list_per_model(local_model))
        else:
            context['models'].append(list_per_model(model))
    context['load_target'] = '#center-panel'
    context['load_next'] = request.GET.get('next', '')  # #704 Ability to load the center panel URL with a ?next=/setup/DirectSpread/1/ argument
    return render(request, 'ScenarioCreator/3Panels.html', context)

# Utility Views was moved to the ADSMSettings/connection_handler.py

def open_population(request, target):
    from ADSMSettings.models import SmSession
    session = SmSession.objects.get()
    session.set_population_upload_status("Processing file")

    return parse_population(workspace_path(target), session)


def upload_population(request):
    from ADSMSettings.models import SmSession
    session = SmSession.objects.get()
    if 'GET' in request.method:
        json_response = {"status": session.population_upload_status, "percent": session.population_upload_percent*100} 
        return JsonResponse(json_response)

    session.set_population_upload_status("Processing file")
    if 'filename' in request.POST:
        file_path = workspace_path(request.POST.get('filename')) 
    else:
        try:
            file_path = handle_file_upload(request, is_temp_file=True, overwrite_ok=True)
        except FileExistsError:
            return JsonResponse({"status": "failed", 
                                 "message": "Cannot import file because a file with the same name already exists in the list below."})

    return parse_population(file_path, session)


def parse_population(file_path, session):
    from xml.etree.ElementTree import ParseError
    try:
        model = Population(source_file=file_path)
        model.save()
    except (EOFError, ParseError, BaseException) as error:
        session.set_population_upload_status(status='Failed: %s' % error)
        message = "This is not a valid Population file: " if isinstance(error, ParseError) else ""
        return JsonResponse({"status": "failed", "message": message + str(error)})  # make sure to cast errors to string first
    # wait for Population parsing (up to 5 minutes)
    session.reset_population_upload_status()
    convert_user_notes_to_unit_id()
    return JsonResponse({"status": "complete", "redirect": "/setup/Populations/"})

def export_population(request, format):
    parser = ScenarioCreator.population_parser.ExportPopulation(format)
    parser.export()
    return redirect("/setup/Populations/")


def filtering_params(request):
    """Collects the list of parameters to filter by.  Because of the way this is setup:
    1) Only keys mentioned in this list will be used (security, functionality).
    2) Only one filter for each choice key can be used (e.g. only one production_type__name)"""
    params = {}
    keys = ['latitude__gte', 'latitude__eq', 'latitude__lte', 'longitude__gte', 'longitude__eq',
            'longitude__lte', 'initial_size__gte', 'initial_size__eq', 'initial_size__lte',  # 3 permutations for each number field
            'production_type__name', 'initial_state']
    if request:
        for key in keys:
            if key in request.GET:
                params[key] = request.GET.get(key)
    return params


def filter_info(request, params):
    """Provides the information necessary for Javascript to fully construct a set of filters for Population"""
    info = {}
    # each select option
    info['select_fields'] = {'production_type__name': [x.name for x in ProductionType.objects.all()],
                             'initial_state': Unit.initial_state_choices}
    info['numeric_fields'] = ["latitude","longitude", "initial_size"]
    info['remaining_filters'] = [x for x in info['select_fields'] if x not in params.keys()]
    return info


def population(request):
    """"Creates the formset and filter context for Population View"""
    context = {}
    FarmSet = modelformset_factory(Unit, extra=0, form=UnitFormAbbreviated, can_delete=False)
    if save_formset_succeeded(FarmSet, Unit, context, request):
        return redirect(request.path)
    if Population.objects.filter(id=1, ).exists():

        if not Unit.objects.count(): # #571 no units were imported: error, blank files
            Population.objects.all().delete()
            return population(request)  # delete blank and try again

        sort_type = request.GET.get('sort_by', 'initial_state')
        query_filter = Q()
        params = filtering_params(request)
        for key, value in params.items():  # loops through params and stacks filters in an AND fashion
            query_filter = query_filter & Q(**{key: value})

        initialized_formset = FarmSet(queryset=Unit.objects.filter(query_filter).order_by(sort_type)[:100])
        context['formset'] = initialized_formset
        context['filter_info'] = filter_info(request, params)
        context['deletable'] = '/setup/Population/1/delete/'
        context['editable'] = request.GET.get('readonly', 'editable')
        context['population_file'] = os.path.basename(Population.objects.get().source_file)
        context['Population'] = Unit.objects.count()
        context['Farms'] = Unit.objects.count()
    else:
        context['xml_files'] = file_list([".xml", ".csv"])
    return render(request, 'ScenarioCreator/Population.html', context)


def validate_scenario(request):

    # ensure that the destruction_reason_order includes all elements. See #990 for more details
    dg = DestructionGlobal.objects.all().first()
    if dg:
        DestructionGlobal.objects.filter(pk=1).update(destruction_reason_order=match_data(dg.destruction_reason_order, "Basic, Trace fwd direct, Trace fwd indirect, Trace back direct, Trace back indirect, Ring"))

    simulation = subprocess.Popen(adsm_executable_command() + ['--dry-run'],
                                  shell=(platform.system() != 'Darwin'),
                                  stdout=subprocess.PIPE,
                                  stderr=subprocess.PIPE)
    stdout, stderr = simulation.communicate()  # still running while we work on python validation
    
    simulation.wait()  # simulation will process db then exit
    print("C Engine Exit Code:", simulation.returncode)
    context = {'dry_run_passed': simulation.returncode == 0 and not stderr,
               'sim_output': stdout.decode() + stderr.decode(),
               'whole_scenario_warnings': whole_scenario_validation(),
               'base_page': 'ScenarioCreator/Validation.html'}
    return render(request, 'ScenarioCreator/MainPanel.html', context)


def vaccination_global(request):
    instance = VaccinationGlobal.objects.get()
    initialized_form = VaccinationMasterForm(request.POST or None, instance=instance)
    if request.method == "POST":
        if initialized_form.is_valid():
            instance = initialized_form.save(commit=True)
    context = {
        'title': 'Vaccination Global',
        'ordering': json.loads(instance.vaccination_priority_order, object_pairs_hook=OrderedDict),
        'form': initialized_form
    }

    return render(request, 'ScenarioCreator/VaccinationGlobal.html', context)


def destruction_global(request):

    instance = DestructionGlobal.objects.get()
    initialized_form = DestructionMasterForm(request.POST or None, instance=instance)
    if request.method == "POST":
        if initialized_form.is_valid():
            instance = initialized_form.save(commit=True)

    context = {
        'title': 'Destruction Global',
        'reasons': match_data(instance.destruction_reason_order, "Basic, Trace fwd direct, Trace fwd indirect, Trace back direct, Trace back indirect, Ring").split(","),
        'priorities': instance.destruction_priority_order.split(","),
        'form': initialized_form,
    }
    '''
    #Destruction Priority Secondary Priority
    'priorities': json.loads(json.dumps(match_data(str(instance.destruction_priority_order), '{"Days Holding":["Oldest", "Newest"], "Production Type":[], "Size":["Largest", "Smallest"]}')), object_pairs_hook=OrderedDict),
    '''

    return render(request, 'ScenarioCreator/DestructionGlobal.html', context)


def match_data(current, all_data):

    def try_dict(current_dict, all_data_dict):
        if "{" in current_dict and "{" in all_data_dict:
            try:
                try:
                    all_data_dict = json.loads(all_data_dict, object_pairs_hook=OrderedDict)
                except ValueError:
                    return None
                except SyntaxError:
                    return current_dict
                try:
                    current_dict = json.loads(current_dict, object_pairs_hook=OrderedDict)
                except ValueError:
                    return None
                except SyntaxError:
                    return all_data_dict
                if isinstance(current_dict, dict):
                    for key in all_data_dict:
                        current_dict.setdefault(key, all_data_dict[key])
                    return current_dict
            except ValueError:
                return None

    dict_return = try_dict(current, all_data)
    if dict_return is not None:
        return dict_return

    was_string = False
    if isinstance(current, str):
        was_string = True
        current = current.replace(", ", ",").split(",")
        all_data = all_data.replace(", ", ",").split(",")

    for element in all_data:
        if element not in current:
            current.append(element)
    for element in current:
        if element not in all_data:
            current.remove(element)

    if was_string:
        current = ",".join(current)

    return current
