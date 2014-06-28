from django.db import models
import Results.output_parser
from ScenarioCreator.models import ProductionType, Zone
import re

"""Results models explanation: The Results models are containers to capture all of the output generated by the CEngine
simulation and present it to the user broken down into 13 different tables.

Note: We are not storing cumulative values at the moment, since it can be computed.

Model Declarations: Each model creates a table in sqlite3 and a 'model' for table presentation on the GUI.  So
 each model serves double duty.  Notice that there are effectively 3 names for each field inside a model.
 1) the Python name (e.g. tsdASusc = models.) is used when constructing the object and is designed to match the CEngine output.
 2) the db_column name will show up when a user exports the DataBase.  They are at least readable explanations.
 3) verbose_name is used in the GUI for displaying Table headers.  Without this, Django would use the Python name,
 which is significantly more obscure.
 The code in scripts/Output_Table.py (.ipynb) was used to generate these name declarations.  Also, if you're reading this
 doc and you don't know about IPython Notebooks, go get IPython Notebooks."""


def printable_name(underscores_name):
    underscores_name = re.sub(r'([a-z])([A-Z])', r'\1_\2', underscores_name).lower()  # convert from camel case
    spaced = re.sub(r'_', r' ', underscores_name)
    return spaced.title()  # capitalize
    #TODO: Add the explain[] dictionary to the printable names, split on spaces, and look for matching strings


class OutputBaseModel(models.Model):
    def __iter__(self):
        for field in self._meta.fields:
            # try:
            #     value = getattr(self, field)
            # except:
            #     value = None
            yield (field.name, field)
    # This lets; you; do:
    # for field, val in myModel:
    #     print( field, val)
    class Meta:
        abstract = True


class OutputManager(models.Manager):
    def bulk_create(self, header_line, cmd_strings, *args, **kwargs):
        headers = header_line.split(',')
        report_objects = []
        for cmd_string in cmd_strings:
            sparse_values = {}
            values = cmd_string.split(',')
            pairs = zip(headers, values)
            for key, value in pairs:
                if value:# and value != '0':
                    sparse_values[key] = int(value)
            report_objects.append(DailyReport(sparse_dict=str(sparse_values), full_line=cmd_string))
            Results.output_parser.populate_db_from_daily_report(sparse_values)
        # for obj in report_objects:
        #     print(obj)  #.save()
        return super().bulk_create(report_objects)


class DailyReport(OutputBaseModel):
    sparse_dict = models.TextField()
    full_line = models.TextField()
    # to get the dictionary object back:
    # import ast
    # ast.literal_eval("{'muffin' : 'lolz', 'foo' : 'kitty'}")

    objects = OutputManager()

    def __str__(self):
        return self.sparse_dict


class SpreadGroup(OutputBaseModel):
    UAll = models.IntegerField(blank=True, null=True, verbose_name="Unit All Spread Types")
    UDir = models.IntegerField(blank=True, null=True, verbose_name="Unit Direct")
    UInd = models.IntegerField(blank=True, null=True, verbose_name="Unit Indirect")
    UAir = models.IntegerField(blank=True, null=True, verbose_name="Unit Air")
    UIni = models.IntegerField(blank=True, null=True, verbose_name="Unit Initial")

    AAll = models.IntegerField(blank=True, null=True, verbose_name="Animal All Spread Types")
    ADir = models.IntegerField(blank=True, null=True, verbose_name="Animal Direct")
    AInd = models.IntegerField(blank=True, null=True, verbose_name="Animal Indirect")
    AAir = models.IntegerField(blank=True, null=True, verbose_name="Animal Air")
    AIni = models.IntegerField(blank=True, null=True, verbose_name="Unit Initial")


class DetectionBracketGroup(OutputBaseModel):
    _blank = models.IntegerField(blank=True, null=True, verbose_name="either method")
    Clin = models.IntegerField(blank=True, null=True, verbose_name="Detection from Clinical signs")
    Test = models.IntegerField(blank=True, null=True, verbose_name="Detection from Lab Tests")


class DetectionGroup(OutputBaseModel):
    UAll = models.IntegerField(blank=True, null=True, verbose_name="Units from Either method")
    UClin = models.IntegerField(blank=True, null=True, verbose_name="Units from Clinical signs")
    UTest = models.IntegerField(blank=True, null=True, verbose_name="Units from Lab Tests")

    AAll = models.IntegerField(blank=True, null=True, verbose_name="Animals from Either method")
    AClin = models.IntegerField(blank=True, null=True, verbose_name="Animals from Clinical signs")
    ATest = models.IntegerField(blank=True, null=True, verbose_name="Animals from Lab Tests")


class TraceGroup(OutputBaseModel):
    UAll = models.IntegerField(blank=True, null=True, verbose_name="Units from Either method ")
    UAllp = models.IntegerField(blank=True, null=True, verbose_name="Units from Either method Possible")
    UDir = models.IntegerField(blank=True, null=True, verbose_name="Units Direct Spread ")
    UDirp = models.IntegerField(blank=True, null=True, verbose_name="Units Direct Spread Possible")
    UInd = models.IntegerField(blank=True, null=True, verbose_name="Units Indirect Spread ")
    UIndp = models.IntegerField(blank=True, null=True, verbose_name="Units Indirect Spread Possible")

    AAll = models.IntegerField(blank=True, null=True, verbose_name="Animals from Either method ")
    AAllp = models.IntegerField(blank=True, null=True, verbose_name="Animals from Either method Possible")
    ADir = models.IntegerField(blank=True, null=True, verbose_name="Animals Direct Spread ")
    ADirp = models.IntegerField(blank=True, null=True, verbose_name="Animals Direct Spread Possible")
    AInd = models.IntegerField(blank=True, null=True, verbose_name="Animals Indirect Spread ")
    AIndp = models.IntegerField(blank=True, null=True, verbose_name="Animals Indirect Spread Possible")


class TestTriggerGroup(OutputBaseModel):
    UAll = models.IntegerField(blank=True, null=True, verbose_name="Units from Any Cause")
    URing = models.IntegerField(blank=True, null=True, verbose_name="Units because of Ring")
    UDirFwd = models.IntegerField(blank=True, null=True, verbose_name="Units because of Direct Forward trace")
    UIndFwd = models.IntegerField(blank=True, null=True, verbose_name="Units because of Indirect Forward trace")
    UDirBack = models.IntegerField(blank=True, null=True, verbose_name="Units because of Direct Back trace")
    UIndBack = models.IntegerField(blank=True, null=True, verbose_name="Units because of Indirect Back trace")
    UDet = models.IntegerField(blank=True, null=True, verbose_name="Units ")

    AAll = models.IntegerField(blank=True, null=True, verbose_name="Animals from Any Cause")
    ARing = models.IntegerField(blank=True, null=True, verbose_name="Animals because of Ring")
    ADirFwd = models.IntegerField(blank=True, null=True, verbose_name="Animals because of Direct Forward trace")
    AIndFwd = models.IntegerField(blank=True, null=True, verbose_name="Animals because of Indirect Forward trace")
    ADirBack = models.IntegerField(blank=True, null=True, verbose_name="Animals because of Direct Back trace")
    AIndBack = models.IntegerField(blank=True, null=True, verbose_name="Animals because of Indirect Back trace")
    ADet = models.IntegerField(blank=True, null=True, verbose_name="Animals ")


class TestOutcomeGroup(OutputBaseModel):
    UTruePos = models.IntegerField(blank=True, null=True, verbose_name="Units True Positives")
    UFalsePos = models.IntegerField(blank=True, null=True, verbose_name="Units False Positives")
    UTrueNeg = models.IntegerField(blank=True, null=True, verbose_name="Units True Negatives")
    UFalseNeg = models.IntegerField(blank=True, null=True, verbose_name="Units False Negatives")


class VaccinationGroup(OutputBaseModel):
    UAll = models.IntegerField(blank=True, null=True, verbose_name="Units from Either method")
    UIni = models.IntegerField(blank=True, null=True, verbose_name="Units Initially")
    URing = models.IntegerField(blank=True, null=True, verbose_name="Units because of Ring")
    AAll = models.IntegerField(blank=True, null=True, verbose_name="Animals from Either method")
    AIni = models.IntegerField(blank=True, null=True, verbose_name="Animals Initially")
    ARing = models.IntegerField(blank=True, null=True, verbose_name="Animals because of Ring")


class WaitGroup(OutputBaseModel):
    UAll = models.IntegerField(blank=True, null=True,
        help_text="")
    AAll = models.IntegerField(blank=True, null=True,
        help_text="")
    UMax = models.IntegerField(blank=True, null=True,
        help_text="Maximum number of units in queue for <action> on any given day over the course of the iteration")
    UMaxDay = models.IntegerField(blank=True, null=True,
        help_text="The first simulation day on which the maximum number of units in queue for <action> was reached")
    AMax = models.IntegerField(blank=True, null=True,
        help_text="Maximum number of animals in queue for <action> on any given day over the course of the iteration")
    AMaxDay = models.IntegerField(blank=True, null=True,
        help_text="The first simulation day on which the maximum number of animals in queue for <action> was reached")
    UTimeMax = models.IntegerField(blank=True, null=True,
        help_text="Maximum number of days spent in queue for <action> by any single unit over the course of the iteration")
    UTimeAvg = models.IntegerField(blank=True, null=True,
        help_text="Average number of days spent in queue for <action> by each unit that was vaccinated over the course of the iteration")
    UDaysInQueue = models.IntegerField(blank=True, null=True,
        help_text="Number of Unit Days waiting in Queue")
    ADaysInQueue = models.IntegerField(blank=True, null=True,
        help_text="Number of Animal Days waiting in Queue")


class DestructionGroup(OutputBaseModel):
    _blank = models.IntegerField(blank=True, null=True, verbose_name="All")
    All = models.IntegerField(blank=True, null=True, verbose_name="All")
    Unsp = models.IntegerField(blank=True, null=True, verbose_name="Unspecified")
    Ring = models.IntegerField(blank=True, null=True, verbose_name="because of Ring")
    Det = models.IntegerField(blank=True, null=True, verbose_name="because of Detection")
    Ini = models.IntegerField(blank=True, null=True, verbose_name="Initially")
    DirFwd = models.IntegerField(blank=True, null=True, verbose_name="because of Direct Forward trace")
    IndFwd = models.IntegerField(blank=True, null=True, verbose_name="because of Indirect Forward trace")
    DirBack = models.IntegerField(blank=True, null=True, verbose_name="because of Direct Back trace")
    IndBack = models.IntegerField(blank=True, null=True, verbose_name="because of Indirect Back trace")


class StateGroup(OutputBaseModel):
    # Note that the ProductionType is in the middle of this field:
    # grammars['tsd'] = [('U','A'), ('','_Bull_','_Swine_'), ('Susc','Lat','Subc','Clin','NImm','VImm','Dest')]
    USusc = models.IntegerField(blank=True, null=True, verbose_name="Units Susceptible")  # Possibly "Units became Susceptible"
    ULat = models.IntegerField(blank=True, null=True, verbose_name="Units Latent")
    USubc = models.IntegerField(blank=True, null=True, verbose_name="Units Subclinical")
    UClin = models.IntegerField(blank=True, null=True, verbose_name="Units Clinical")
    UNImm = models.IntegerField(blank=True, null=True, verbose_name="Units Natural Immune")
    UVImm = models.IntegerField(blank=True, null=True, verbose_name="Units Vaccine Immune")
    UDest = models.IntegerField(blank=True, null=True, verbose_name="Units Destroyed")

    ASusc = models.IntegerField(blank=True, null=True, verbose_name="Animals Susceptible")
    ALat = models.IntegerField(blank=True, null=True, verbose_name="Animals Latent")
    ASubc = models.IntegerField(blank=True, null=True, verbose_name="Animals Subclinical")
    AClin = models.IntegerField(blank=True, null=True, verbose_name="Animals Clinical")
    ANImm = models.IntegerField(blank=True, null=True, verbose_name="Animals Natural Immune")
    AVImm = models.IntegerField(blank=True, null=True, verbose_name="Animals Vaccine Immune")
    ADest = models.IntegerField(blank=True, null=True, verbose_name="Animals Destroyed")


class DailyByProductionType(OutputBaseModel):
    iteration = models.IntegerField(blank=True, null=True, verbose_name=printable_name('iteration'),
        help_text='The iteration during which the outputs in this records where generated.', )
    day = models.IntegerField(blank=True, null=True, verbose_name=printable_name('day'),
        help_text='The day in this iteration during which the outputs in this records where generated.', )
    production_type = models.ForeignKey(ProductionType, blank=True, null=True, verbose_name=printable_name('production_type'),
        help_text='The identifier of the production type that these outputs apply to.', )

    exp = models.ForeignKey(SpreadGroup, related_name='+', blank=True, null=True, verbose_name="Exposures")
    inf = models.ForeignKey(SpreadGroup, related_name='+', blank=True, null=True, verbose_name="Infections")
    firstDetection = models.ForeignKey(DetectionBracketGroup, related_name='+', blank=True, null=True, verbose_name="First Detection")
    lastDetection = models.ForeignKey(DetectionBracketGroup, related_name='+', blank=True, null=True, verbose_name="Last Detection")
    det = models.ForeignKey(DetectionGroup, related_name='+', blank=True, null=True, verbose_name="Detections")
    tr = models.ForeignKey(TraceGroup, related_name='+', blank=True, null=True, verbose_name="Traces")
    exm = models.ForeignKey(TestTriggerGroup, related_name='+', blank=True, null=True, verbose_name="Examinations")

    #tstcU uses the TestTriggerGroup because of the overlap in Directional causes
    tstc = models.ForeignKey(TestTriggerGroup, related_name='+', blank=True, null=True, verbose_name="Lab Test Triggers")
    #TODO: Check for 'n' or 'c' next.  This is going to need very particular switching to catch the tstnUTruePos, tstcUTruePos, tstcUDirFwd
    #we need a second model to catch True/False Pos/Neg results
    tst = models.ForeignKey(TestOutcomeGroup, related_name='+', blank=True, null=True, verbose_name="Lab Test Outcomes")

    #This group of two was so small I didn't think it warranted a group object
    firstVaccination = models.IntegerField(    blank=True, null=True, verbose_name="First Vaccination")
    firstVaccinationRing = models.IntegerField(blank=True, null=True, verbose_name="First Vaccination caused by a Ring")

    vac = models.ForeignKey(VaccinationGroup, related_name='+', blank=True, null=True, verbose_name="Vaccinations")
    vacw = models.ForeignKey(WaitGroup, related_name='+', blank=True, null=True, verbose_name="Vaccination Wait")

    firstDestruction = models.ForeignKey(DestructionGroup, related_name='+', blank=True, null=True, verbose_name="First Destruction")
    #These two separate U and A so that they can use the same Group object as firstDestruction
    desnU = models.ForeignKey(DestructionGroup, related_name='+', blank=True, null=True, verbose_name="Destruction of Units")
    desnA = models.ForeignKey(DestructionGroup, related_name='+', blank=True, null=True, verbose_name="Destruction of Animals")
    desw = models.ForeignKey(WaitGroup, related_name='+', blank=True, null=True, verbose_name="Destruction Wait")

    tsd = models.ForeignKey(StateGroup, related_name='+', blank=True, null=True, verbose_name="Transition State Daily")


#####END DailyByProductionType######

#####BEGIN DailyByZoneAndProductionType######


class DailyByZoneAndProductionType(OutputBaseModel):
    iteration = models.IntegerField(blank=True, null=True, verbose_name=printable_name('iteration'),
        help_text='The iteration during which the outputs in this records where generated.', )
    day = models.IntegerField(blank=True, null=True, verbose_name=printable_name('day'),
        help_text='The day in this iteration during which the outputs in this records where generated.', )
    production_type = models.ForeignKey(ProductionType, blank=True, null=True, verbose_name=printable_name('production_type'),
        help_text='The identifier of the production type that these outputs apply to.', )
    zone = models.ForeignKey(Zone, blank=True, null=True, verbose_name=printable_name('zone'),
        help_text='The identifier of the zone that these outputs apply to.', )

    unitsInZone      = models.IntegerField(blank=True, null=True, verbose_name=printable_name('unitsInZone'))
    unitDaysInZone   = models.IntegerField(blank=True, null=True, verbose_name=printable_name('unitDaysInZone'))
    animalDaysInZone = models.IntegerField(blank=True, null=True, verbose_name=printable_name('animalDaysInZone'))

    def __str__(self):
        return "%i, %i: %s and %s" % (self.iteration, self.day, self.production_type or "All Types", self.zone or "Background")


class DailyByZone(OutputBaseModel):
    iteration = models.IntegerField(blank=True, null=True, verbose_name=printable_name('iteration'),
        help_text='The iteration during which the outputs in this records where generated.', )
    day = models.IntegerField(blank=True, null=True, verbose_name=printable_name('day'),
        help_text='The day in this iteration during which the outputs in this records where generated.', )
    zone = models.ForeignKey(Zone, blank=True, null=True, verbose_name=printable_name('zone'),
        help_text='The identifier of the zone that these outputs apply to.', )

    zoneArea            = models.IntegerField(blank=True, null=True, verbose_name=printable_name('zoneArea'))
    maxZoneArea         = models.IntegerField(blank=True, null=True, verbose_name=printable_name('maxZoneArea'))
    maxZoneAreaDay      = models.IntegerField(blank=True, null=True, verbose_name=printable_name('maxZoneAreaDay'))
    zonePerimeter       = models.IntegerField(blank=True, null=True, verbose_name=printable_name('zonePerimeter'))
    maxZonePerimeter    = models.IntegerField(blank=True, null=True, verbose_name=printable_name('maxZonePerimeter'))
    maxZonePerimeterDay = models.IntegerField(blank=True, null=True, verbose_name=printable_name('maxZonePerimeterDay'))
    finalZoneArea       = models.IntegerField(blank=True, null=True, verbose_name=printable_name('finalZoneArea'))
    finalZonePerimeter  = models.IntegerField(blank=True, null=True, verbose_name=printable_name('finalZonePerimeter'))
    num_separate_areas  = models.IntegerField(blank=True, null=True, verbose_name=printable_name('num_separate_areas'))


class DailyControls(OutputBaseModel):
    iteration = models.IntegerField(blank=True, null=True, verbose_name=printable_name('iteration'),
        help_text='The iteration during which the outputs in this records where generated.', )
    day = models.IntegerField(blank=True, null=True, verbose_name=printable_name('day'),
        help_text='The day in this iteration during which the outputs in this records where generated.', )

    diseaseDuration      = models.IntegerField(blank=True, null=True, verbose_name=printable_name('diseaseDuration'))
    adqnUAll             = models.IntegerField(blank=True, null=True, verbose_name=printable_name('New Units Adequately Exposed'))
    adqcUAll             = models.IntegerField(blank=True, null=True, verbose_name=printable_name('Cumulative Units Adequately Exposed'))
    detOccurred          = models.IntegerField(blank=True, null=True, verbose_name=printable_name('detOccurred'))
    costSurveillance     = models.IntegerField(blank=True, null=True, verbose_name=printable_name('costSurveillance'))
    vaccOccurred         = models.IntegerField(blank=True, null=True, verbose_name=printable_name('vaccOccurred'))
    vacwUMax             = models.IntegerField(blank=True, null=True, verbose_name=printable_name('vacwUMax'))
    vacwUMaxDay          = models.IntegerField(blank=True, null=True, verbose_name=printable_name('vacwUMaxDay'))
    vacwUDaysInQueue     = models.IntegerField(blank=True, null=True, verbose_name=printable_name('vacwUDaysInQueue'))
    vacwUTimeAvg         = models.IntegerField(blank=True, null=True, verbose_name=printable_name('vacwUTimeAvg'))
    vacwUTimeMax         = models.IntegerField(blank=True, null=True, verbose_name=printable_name('vacwUTimeMax'))
    vacwAMax             = models.IntegerField(blank=True, null=True, verbose_name=printable_name('vacwAMax'))
    vacwAMaxDay          = models.IntegerField(blank=True, null=True, verbose_name=printable_name('vacwAMaxDay'))
    vacwADaysInQueue     = models.IntegerField(blank=True, null=True, verbose_name=printable_name('vacwADaysInQueue'))
    vaccSetup            = models.IntegerField(blank=True, null=True, verbose_name=printable_name('vaccSetup'))
    vaccVaccination      = models.IntegerField(blank=True, null=True, verbose_name=printable_name('vaccVaccination'))
    vaccSubtotal         = models.IntegerField(blank=True, null=True, verbose_name=printable_name('vaccSubtotal'))
    destrOccurred        = models.IntegerField(blank=True, null=True, verbose_name=printable_name('destrOccurred'))
    deswUMax             = models.IntegerField(blank=True, null=True, verbose_name=printable_name('deswUMax'))
    deswUMaxDay          = models.IntegerField(blank=True, null=True, verbose_name=printable_name('deswUMaxDay'))
    deswUDaysInQueue     = models.IntegerField(blank=True, null=True, verbose_name=printable_name('deswUDaysInQueue'))
    deswUTimeAvg         = models.IntegerField(blank=True, null=True, verbose_name=printable_name('deswUTimeAvg'))
    deswUTimeMax         = models.IntegerField(blank=True, null=True, verbose_name=printable_name('deswUTimeMax'))
    deswAMax             = models.IntegerField(blank=True, null=True, verbose_name=printable_name('deswAMax'))
    deswAMaxDay          = models.IntegerField(blank=True, null=True, verbose_name=printable_name('deswAMaxDay'))
    deswADaysInQueue     = models.IntegerField(blank=True, null=True, verbose_name=printable_name('deswADaysInQueue'))
    destrAppraisal       = models.IntegerField(blank=True, null=True, verbose_name=printable_name('destrAppraisal'))
    destrEuthanasia      = models.IntegerField(blank=True, null=True, verbose_name=printable_name('destrEuthanasia'))
    destrIndemnification = models.IntegerField(blank=True, null=True, verbose_name=printable_name('destrIndemnification'))
    destrDisposal        = models.IntegerField(blank=True, null=True, verbose_name=printable_name('destrDisposal'))
    destrCleaning        = models.IntegerField(blank=True, null=True, verbose_name=printable_name('destrCleaning'))
    destrSubtotal        = models.IntegerField(blank=True, null=True, verbose_name=printable_name('destrSubtotal'))
    outbreakDuration     = models.IntegerField(blank=True, null=True, verbose_name=printable_name('outbreakDuration'))
    costsTotal           = models.IntegerField(blank=True, null=True, verbose_name=printable_name('costsTotal'))
    firstDetUInfAll      = models.IntegerField(blank=True, null=True, verbose_name=printable_name('Units Infected at First Detection'))
    firstDetAInfAll      = models.IntegerField(blank=True, null=True, verbose_name=printable_name('Animals Infected at First Detection'))
    ratio                = models.IntegerField(blank=True, null=True, verbose_name=printable_name('ratio'))
    average_prevalence   = models.IntegerField(blank=True, null=True, verbose_name=printable_name('average_prevalence'))
    detcUqAll            = models.IntegerField(blank=True, null=True, verbose_name=printable_name('detcUqAll'))


