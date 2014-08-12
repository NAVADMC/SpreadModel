from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
from collections import OrderedDict
from future import standard_library
standard_library.install_hooks()
from future.builtins import object

from Results.models import DailyControls, DailyByProductionType, DailyByZone
from ScenarioCreator.models import Zone
from django.db.models import Q, F


def list_of_iterations():
    return list(DailyControls.objects.values_list('iteration', flat=True).distinct())


def median_value(queryset, term):
    count = queryset.count()
    return queryset.values_list(term, flat=True).order_by(term)[int(round(count/2))]


def last_day_query():
    last_days = {}  # dictionary with iteration int keys
    for iteration in list_of_iterations():
        last_days[iteration] = DailyControls.objects.filter(iteration=iteration).order_by('day').last().day
    last_day_query1 = [Q(iteration=key, day=value) for key, value in last_days.items()]
    return reduce(Q.__or__, last_day_query1, Q(day=-1))


def field_summary(field_name, model=DailyByProductionType):
    # switch on model
    if model == DailyByProductionType:  # query only the "All" production type on the last day of each iteration
        queryset = DailyByProductionType.objects.filter(last_day_query(), production_type=None)
    elif model == DailyControls:
        queryset = DailyControls.objects.filter(last_day_query())
    else:  # zone
        zone = Zone.objects.all().order_by('radius').last()
        queryset = DailyByZone.objects.filter(last_day_query(), zone=zone)

    return median_value(queryset, field_name)  # value list, last day, median, aggregate


def name(field_name, model=DailyByProductionType):
    return model._meta.get_field_by_name(field_name)[0].verbose_name


def name_and_value(field_name, model=DailyByProductionType):
    return name(field_name, model), field_summary(field_name, model)


def pair(unit_pair, animal_number):
    return unit_pair[0], "%i (%i)" % (unit_pair[1], animal_number)


def summarize_results():
    summary = OrderedDict()
    summary["Unit (Animal) Summary"] = {
        pair(name_and_value("infcU"), field_summary("infcA")),
        pair(name_and_value("firstDetUInfAll", DailyControls), field_summary("firstDetAInfAll", DailyControls)),
        pair(name_and_value("descUAll"), field_summary("descAAll")),
        pair(name_and_value("vaccUAll"), field_summary("vaccAAll"))}
    # summary["Animal Summary"] = {
    #     name_and_value("infcA"),
    #     name_and_value("firstDetAInfAll", DailyControls),
    #     name_and_value("descAAll"),
    #     name_and_value("vaccAAll")}
    summary["Days Summary"] = {
        name_and_value("outbreakDuration", DailyControls),
        name_and_value("diseaseDuration", DailyControls),
        name_and_value("firstDetection"),
        name_and_value("firstVaccination"),
        name_and_value("firstDestruction")}
    summary["Zone Summary"] = {name_and_value("maxZoneArea", DailyByZone)}

    return summary
