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
import re
from ast import literal_eval
from django.db import models

from ScenarioCreator.models import ProductionType, Zone, Unit
from Results.output_grammar import explain


def printable_name(underscores_name):
    underscores_name = re.sub(r'([a-z])([A-Z])', r'\1_\2', underscores_name).lower()  # convert from camel case
    spaced = re.sub(r'_', r' ', underscores_name)
    return spaced.title()  # capitalize


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
    class Meta(object):
        abstract = True


class DailyReport(OutputBaseModel):
    sparse_dict = models.TextField()
    full_line = models.TextField()

    def __str__(self):
        sparse_dict = literal_eval(self.sparse_dict)
        return "iteration: %s, day: %s" % (sparse_dict['Run'], sparse_dict['Day'])


class DailyByProductionType(OutputBaseModel):
    iteration = models.IntegerField(blank=True, null=True, verbose_name=printable_name('iteration'),
        help_text='The iteration during which the outputs in this records where generated.', )
    day = models.IntegerField(blank=True, null=True, verbose_name=printable_name('day'),
        help_text='The day in this iteration during which the outputs in this records where generated.', )
    last_day = models.BooleanField(default=False, help_text="Flag that is only set on the last day of an iteration.")
    production_type = models.ForeignKey(ProductionType, blank=True, null=True, verbose_name=printable_name('production_type'),
        help_text='The identifier of the production type that these outputs apply to.', )

    desnU = models.IntegerField(blank=True, null=True, verbose_name=explain("desnU"))
    desnURing = models.IntegerField(blank=True, null=True, verbose_name=explain("desnURing"))
    desnUDet = models.IntegerField(blank=True, null=True, verbose_name=explain("desnUDet"))
    desnUIni = models.IntegerField(blank=True, null=True, verbose_name=explain("desnUIni"))
    desnUDirFwd = models.IntegerField(blank=True, null=True, verbose_name=explain("desnUDirFwd"))
    desnUIndFwd = models.IntegerField(blank=True, null=True, verbose_name=explain("desnUIndFwd"))
    desnUDirBack = models.IntegerField(blank=True, null=True, verbose_name=explain("desnUDirBack"))
    desnUIndBack = models.IntegerField(blank=True, null=True, verbose_name=explain("desnUIndBack"))
    desnA = models.IntegerField(blank=True, null=True, verbose_name=explain("desnA"))
    desnARing = models.IntegerField(blank=True, null=True, verbose_name=explain("desnARing"))
    desnADet = models.IntegerField(blank=True, null=True, verbose_name=explain("desnADet"))
    desnAIni = models.IntegerField(blank=True, null=True, verbose_name=explain("desnAIni"))
    desnADirFwd = models.IntegerField(blank=True, null=True, verbose_name=explain("desnADirFwd"))
    desnAIndFwd = models.IntegerField(blank=True, null=True, verbose_name=explain("desnAIndFwd"))
    desnADirBack = models.IntegerField(blank=True, null=True, verbose_name=explain("desnADirBack"))
    desnAIndBack = models.IntegerField(blank=True, null=True, verbose_name=explain("desnAIndBack"))
    descU = models.IntegerField(blank=True, null=True, verbose_name=explain("descU"))
    descURing = models.IntegerField(blank=True, null=True, verbose_name=explain("descURing"))
    descUDet = models.IntegerField(blank=True, null=True, verbose_name=explain("descUDet"))
    descUIni = models.IntegerField(blank=True, null=True, verbose_name=explain("descUIni"))
    descUDirFwd = models.IntegerField(blank=True, null=True, verbose_name=explain("descUDirFwd"))
    descUIndFwd = models.IntegerField(blank=True, null=True, verbose_name=explain("descUIndFwd"))
    descUDirBack = models.IntegerField(blank=True, null=True, verbose_name=explain("descUDirBack"))
    descUIndBack = models.IntegerField(blank=True, null=True, verbose_name=explain("descUIndBack"))
    descA = models.IntegerField(blank=True, null=True, verbose_name=explain("descA"))
    descARing = models.IntegerField(blank=True, null=True, verbose_name=explain("descARing"))
    descADet = models.IntegerField(blank=True, null=True, verbose_name=explain("descADet"))
    descAIni = models.IntegerField(blank=True, null=True, verbose_name=explain("descAIni"))
    descADirFwd = models.IntegerField(blank=True, null=True, verbose_name=explain("descADirFwd"))
    descAIndFwd = models.IntegerField(blank=True, null=True, verbose_name=explain("descAIndFwd"))
    descADirBack = models.IntegerField(blank=True, null=True, verbose_name=explain("descADirBack"))
    descAIndBack = models.IntegerField(blank=True, null=True, verbose_name=explain("descAIndBack"))
    deswU = models.IntegerField(blank=True, null=True, verbose_name=explain("deswU"))
    deswA = models.IntegerField(blank=True, null=True, verbose_name=explain("deswA"))
    
    detcU = models.IntegerField(blank=True, null=True, verbose_name=explain("detcU"))
    detcUClin = models.IntegerField(blank=True, null=True, verbose_name=explain("detcUClin"))
    detcUTest = models.IntegerField(blank=True, null=True, verbose_name=explain("detcUTest"))
    detcA = models.IntegerField(blank=True, null=True, verbose_name=explain("detcA"))
    detcAClin = models.IntegerField(blank=True, null=True, verbose_name=explain("detcAClin"))
    detcATest = models.IntegerField(blank=True, null=True, verbose_name=explain("detcATest"))
    detnU = models.IntegerField(blank=True, null=True, verbose_name=explain("detnU"))
    detnUClin = models.IntegerField(blank=True, null=True, verbose_name=explain("detnUClin"))
    detnUTest = models.IntegerField(blank=True, null=True, verbose_name=explain("detnUTest"))
    detnA = models.IntegerField(blank=True, null=True, verbose_name=explain("detnA"))
    detnAClin = models.IntegerField(blank=True, null=True, verbose_name=explain("detnAClin"))
    detnATest = models.IntegerField(blank=True, null=True, verbose_name=explain("detnATest"))
    
    exmnU = models.IntegerField(blank=True, null=True, verbose_name=explain("exmnU"))
    exmnURing = models.IntegerField(blank=True, null=True, verbose_name=explain("exmnURing"))
    exmnUDirFwd = models.IntegerField(blank=True, null=True, verbose_name=explain("exmnUDirFwd"))
    exmnUIndFwd = models.IntegerField(blank=True, null=True, verbose_name=explain("exmnUIndFwd"))
    exmnUDirBack = models.IntegerField(blank=True, null=True, verbose_name=explain("exmnUDirBack"))
    exmnUIndBack = models.IntegerField(blank=True, null=True, verbose_name=explain("exmnUIndBack"))
    exmnUDet = models.IntegerField(blank=True, null=True, verbose_name=explain("exmnUDet"))
    exmnA = models.IntegerField(blank=True, null=True, verbose_name=explain("exmnA"))
    exmnARing = models.IntegerField(blank=True, null=True, verbose_name=explain("exmnARing"))
    exmnADirFwd = models.IntegerField(blank=True, null=True, verbose_name=explain("exmnADirFwd"))
    exmnAIndFwd = models.IntegerField(blank=True, null=True, verbose_name=explain("exmnAIndFwd"))
    exmnADirBack = models.IntegerField(blank=True, null=True, verbose_name=explain("exmnADirBack"))
    exmnAIndBack = models.IntegerField(blank=True, null=True, verbose_name=explain("exmnAIndBack"))
    exmnADet = models.IntegerField(blank=True, null=True, verbose_name=explain("exmnADet"))
    exmcU = models.IntegerField(blank=True, null=True, verbose_name=explain("exmcU"))
    exmcURing = models.IntegerField(blank=True, null=True, verbose_name=explain("exmcURing"))
    exmcUDirFwd = models.IntegerField(blank=True, null=True, verbose_name=explain("exmcUDirFwd"))
    exmcUIndFwd = models.IntegerField(blank=True, null=True, verbose_name=explain("exmcUIndFwd"))
    exmcUDirBack = models.IntegerField(blank=True, null=True, verbose_name=explain("exmcUDirBack"))
    exmcUIndBack = models.IntegerField(blank=True, null=True, verbose_name=explain("exmcUIndBack"))
    exmcUDet = models.IntegerField(blank=True, null=True, verbose_name=explain("exmcUDet"))
    exmcA = models.IntegerField(blank=True, null=True, verbose_name=explain("exmcA"))
    exmcARing = models.IntegerField(blank=True, null=True, verbose_name=explain("exmcARing"))
    exmcADirFwd = models.IntegerField(blank=True, null=True, verbose_name=explain("exmcADirFwd"))
    exmcAIndFwd = models.IntegerField(blank=True, null=True, verbose_name=explain("exmcAIndFwd"))
    exmcADirBack = models.IntegerField(blank=True, null=True, verbose_name=explain("exmcADirBack"))
    exmcAIndBack = models.IntegerField(blank=True, null=True, verbose_name=explain("exmcAIndBack"))
    exmcADet = models.IntegerField(blank=True, null=True, verbose_name=explain("exmcADet"))
    
    expcU = models.IntegerField(blank=True, null=True, verbose_name=explain("expcU"))
    expcUDir = models.IntegerField(blank=True, null=True, verbose_name=explain("expcUDir"))
    expcUInd = models.IntegerField(blank=True, null=True, verbose_name=explain("expcUInd"))
    expcUAir = models.IntegerField(blank=True, null=True, verbose_name=explain("expcUAir"))
    expcA = models.IntegerField(blank=True, null=True, verbose_name=explain("expcA"))
    expcADir = models.IntegerField(blank=True, null=True, verbose_name=explain("expcADir"))
    expcAInd = models.IntegerField(blank=True, null=True, verbose_name=explain("expcAInd"))
    expcAAir = models.IntegerField(blank=True, null=True, verbose_name=explain("expcAAir"))
    expnU = models.IntegerField(blank=True, null=True, verbose_name=explain("expnU"))
    expnUDir = models.IntegerField(blank=True, null=True, verbose_name=explain("expnUDir"))
    expnUInd = models.IntegerField(blank=True, null=True, verbose_name=explain("expnUInd"))
    expnUAir = models.IntegerField(blank=True, null=True, verbose_name=explain("expnUAir"))
    expnA = models.IntegerField(blank=True, null=True, verbose_name=explain("expnA"))
    expnADir = models.IntegerField(blank=True, null=True, verbose_name=explain("expnADir"))
    expnAInd = models.IntegerField(blank=True, null=True, verbose_name=explain("expnAInd"))
    expnAAir = models.IntegerField(blank=True, null=True, verbose_name=explain("expnAAir"))

    adqcU = models.IntegerField(blank=True, null=True, verbose_name=explain("adqcU"))
    adqcUDir = models.IntegerField(blank=True, null=True, verbose_name=explain("adqcUDir"))
    adqcUInd = models.IntegerField(blank=True, null=True, verbose_name=explain("adqcUInd"))
    adqcUAir = models.IntegerField(blank=True, null=True, verbose_name=explain("adqcUAir"))
    adqnU = models.IntegerField(blank=True, null=True, verbose_name=explain("adqnU"))
    adqnUDir = models.IntegerField(blank=True, null=True, verbose_name=explain("adqnUDir"))
    adqnUInd = models.IntegerField(blank=True, null=True, verbose_name=explain("adqnUInd"))
    adqnUAir = models.IntegerField(blank=True, null=True, verbose_name=explain("adqnUAir"))

    firstDestruction = models.IntegerField(blank=True, null=True, verbose_name=explain("firstDestruction"))
    firstDestructionRing = models.IntegerField(blank=True, null=True, verbose_name=explain("firstDestructionRing"))
    firstDestructionDet = models.IntegerField(blank=True, null=True, verbose_name=explain("firstDestructionDet"))
    firstDestructionDirFwd = models.IntegerField(blank=True, null=True, verbose_name=explain("firstDestructionDirFwd"))
    firstDestructionIndFwd = models.IntegerField(blank=True, null=True, verbose_name=explain("firstDestructionIndFwd"))
    firstDestructionDirBack = models.IntegerField(blank=True, null=True, verbose_name=explain("firstDestructionDirBack"))
    firstDestructionIndBack = models.IntegerField(blank=True, null=True, verbose_name=explain("firstDestructionIndBack"))
    firstDetection = models.IntegerField(blank=True, null=True, verbose_name=explain("firstDetection"))
    firstDetectionClin = models.IntegerField(blank=True, null=True, verbose_name=explain("firstDetectionClin"))
    firstDetectionTest = models.IntegerField(blank=True, null=True, verbose_name=explain("firstDetectionTest"))
    firstVaccination = models.IntegerField(blank=True, null=True, verbose_name=explain("firstVaccination"))
    firstVaccinationRing = models.IntegerField(blank=True, null=True, verbose_name=explain("firstVaccinationRing"))
    
    infcU = models.IntegerField(blank=True, null=True, verbose_name=explain("infcU"))
    infcUIni = models.IntegerField(blank=True, null=True, verbose_name=explain("infcUIni"))
    infcUDir = models.IntegerField(blank=True, null=True, verbose_name=explain("infcUDir"))
    infcUInd = models.IntegerField(blank=True, null=True, verbose_name=explain("infcUInd"))
    infcUAir = models.IntegerField(blank=True, null=True, verbose_name=explain("infcUAir"))
    infcA = models.IntegerField(blank=True, null=True, verbose_name=explain("infcA"))
    infcAIni = models.IntegerField(blank=True, null=True, verbose_name=explain("infcAIni"))
    infcADir = models.IntegerField(blank=True, null=True, verbose_name=explain("infcADir"))
    infcAInd = models.IntegerField(blank=True, null=True, verbose_name=explain("infcAInd"))
    infcAAir = models.IntegerField(blank=True, null=True, verbose_name=explain("infcAAir"))
    infnU = models.IntegerField(blank=True, null=True, verbose_name=explain("infnU"))
    infnUIni = models.IntegerField(blank=True, null=True, verbose_name=explain("infnUIni"))
    infnUDir = models.IntegerField(blank=True, null=True, verbose_name=explain("infnUDir"))
    infnUInd = models.IntegerField(blank=True, null=True, verbose_name=explain("infnUInd"))
    infnUAir = models.IntegerField(blank=True, null=True, verbose_name=explain("infnUAir"))
    infnA = models.IntegerField(blank=True, null=True, verbose_name=explain("infnA"))
    infnAIni = models.IntegerField(blank=True, null=True, verbose_name=explain("infnAIni"))
    infnADir = models.IntegerField(blank=True, null=True, verbose_name=explain("infnADir"))
    infnAInd = models.IntegerField(blank=True, null=True, verbose_name=explain("infnAInd"))
    infnAAir = models.IntegerField(blank=True, null=True, verbose_name=explain("infnAAir"))
    
    lastDetection = models.IntegerField(blank=True, null=True, verbose_name=explain("lastDetection"))
    lastDetectionClin = models.IntegerField(blank=True, null=True, verbose_name=explain("lastDetectionClin"))
    lastDetectionTest = models.IntegerField(blank=True, null=True, verbose_name=explain("lastDetectionTest"))
    
    trnU = models.IntegerField(blank=True, null=True, verbose_name=explain("trnU"))
    trnUp = models.IntegerField(blank=True, null=True, verbose_name=explain("trnUp"))
    trnUDir = models.IntegerField(blank=True, null=True, verbose_name=explain("trnUDir"))
    trnUDirp = models.IntegerField(blank=True, null=True, verbose_name=explain("trnUDirp"))
    trnUInd = models.IntegerField(blank=True, null=True, verbose_name=explain("trnUInd"))
    trnUIndp = models.IntegerField(blank=True, null=True, verbose_name=explain("trnUIndp"))
    trnA = models.IntegerField(blank=True, null=True, verbose_name=explain("trnA"))
    trnAp = models.IntegerField(blank=True, null=True, verbose_name=explain("trnAp"))
    trnADir = models.IntegerField(blank=True, null=True, verbose_name=explain("trnADir"))
    trnADirp = models.IntegerField(blank=True, null=True, verbose_name=explain("trnADirp"))
    trnAInd = models.IntegerField(blank=True, null=True, verbose_name=explain("trnAInd"))
    trnAIndp = models.IntegerField(blank=True, null=True, verbose_name=explain("trnAIndp"))
    trcU = models.IntegerField(blank=True, null=True, verbose_name=explain("trcU"))
    trcUp = models.IntegerField(blank=True, null=True, verbose_name=explain("trcUp"))
    trcUDir = models.IntegerField(blank=True, null=True, verbose_name=explain("trcUDir"))
    trcUDirp = models.IntegerField(blank=True, null=True, verbose_name=explain("trcUDirp"))
    trcUInd = models.IntegerField(blank=True, null=True, verbose_name=explain("trcUInd"))
    trcUIndp = models.IntegerField(blank=True, null=True, verbose_name=explain("trcUIndp"))
    trcA = models.IntegerField(blank=True, null=True, verbose_name=explain("trcA"))
    trcAp = models.IntegerField(blank=True, null=True, verbose_name=explain("trcAp"))
    trcADir = models.IntegerField(blank=True, null=True, verbose_name=explain("trcADir"))
    trcADirp = models.IntegerField(blank=True, null=True, verbose_name=explain("trcADirp"))
    trcAInd = models.IntegerField(blank=True, null=True, verbose_name=explain("trcAInd"))
    trcAIndp = models.IntegerField(blank=True, null=True, verbose_name=explain("trcAIndp"))
    
    tsdUSusc = models.IntegerField(blank=True, null=True, verbose_name=explain("tsdUSusc"))
    tsdULat = models.IntegerField(blank=True, null=True, verbose_name=explain("tsdULat"))
    tsdUSubc = models.IntegerField(blank=True, null=True, verbose_name=explain("tsdUSubc"))
    tsdUClin = models.IntegerField(blank=True, null=True, verbose_name=explain("tsdUClin"))
    tsdUNImm = models.IntegerField(blank=True, null=True, verbose_name=explain("tsdUNImm"))
    tsdUVImm = models.IntegerField(blank=True, null=True, verbose_name=explain("tsdUVImm"))
    tsdUDest = models.IntegerField(blank=True, null=True, verbose_name=explain("tsdUDest"))
    tsdASusc = models.IntegerField(blank=True, null=True, verbose_name=explain("tsdASusc"))
    tsdALat = models.IntegerField(blank=True, null=True, verbose_name=explain("tsdALat"))
    tsdASubc = models.IntegerField(blank=True, null=True, verbose_name=explain("tsdASubc"))
    tsdAClin = models.IntegerField(blank=True, null=True, verbose_name=explain("tsdAClin"))
    tsdANImm = models.IntegerField(blank=True, null=True, verbose_name=explain("tsdANImm"))
    tsdAVImm = models.IntegerField(blank=True, null=True, verbose_name=explain("tsdAVImm"))
    tsdADest = models.IntegerField(blank=True, null=True, verbose_name=explain("tsdADest"))
    
    tstcA = models.IntegerField(blank=True, null=True, verbose_name=explain("tstcA"))
    tstcADirFwd = models.IntegerField(blank=True, null=True, verbose_name=explain("tstcADirFwd"))
    tstcAIndFwd = models.IntegerField(blank=True, null=True, verbose_name=explain("tstcAIndFwd"))
    tstcADirBack = models.IntegerField(blank=True, null=True, verbose_name=explain("tstcADirBack"))
    tstcAIndBack = models.IntegerField(blank=True, null=True, verbose_name=explain("tstcAIndBack"))
    tstcU = models.IntegerField(blank=True, null=True, verbose_name=explain("tstcU"))
    tstcUDirFwd = models.IntegerField(blank=True, null=True, verbose_name=explain("tstcUDirFwd"))
    tstcUIndFwd = models.IntegerField(blank=True, null=True, verbose_name=explain("tstcUIndFwd"))
    tstcUDirBack = models.IntegerField(blank=True, null=True, verbose_name=explain("tstcUDirBack"))
    tstcUIndBack = models.IntegerField(blank=True, null=True, verbose_name=explain("tstcUIndBack"))
    tstcUTruePos = models.IntegerField(blank=True, null=True, verbose_name=explain("tstcUTruePos"))
    tstcUFalsePos = models.IntegerField(blank=True, null=True, verbose_name=explain("tstcUFalsePos"))
    tstcUTrueNeg = models.IntegerField(blank=True, null=True, verbose_name=explain("tstcUTrueNeg"))
    tstcUFalseNeg = models.IntegerField(blank=True, null=True, verbose_name=explain("tstcUFalseNeg"))
    tstnU = models.IntegerField(blank=True, null=True, verbose_name=explain("tstnU"))
    tstnUDirFwd = models.IntegerField(blank=True, null=True, verbose_name=explain("tstnUDirFwd"))
    tstnUIndFwd = models.IntegerField(blank=True, null=True, verbose_name=explain("tstnUIndFwd"))
    tstnUDirBack = models.IntegerField(blank=True, null=True, verbose_name=explain("tstnUDirBack"))
    tstnUIndBack = models.IntegerField(blank=True, null=True, verbose_name=explain("tstnUIndBack"))
    tstnUTruePos = models.IntegerField(blank=True, null=True, verbose_name=explain("tstnUTruePos"))
    tstnUFalsePos = models.IntegerField(blank=True, null=True, verbose_name=explain("tstnUFalsePos"))
    tstnUTrueNeg = models.IntegerField(blank=True, null=True, verbose_name=explain("tstnUTrueNeg"))
    tstnUFalseNeg = models.IntegerField(blank=True, null=True, verbose_name=explain("tstnUFalseNeg"))
    
    vaccU = models.IntegerField(blank=True, null=True, verbose_name=explain("vaccU"))
    vaccUIni = models.IntegerField(blank=True, null=True, verbose_name=explain("vaccUIni"))
    vaccURing = models.IntegerField(blank=True, null=True, verbose_name=explain("vaccURing"))
    vaccA = models.IntegerField(blank=True, null=True, verbose_name=explain("vaccA"))
    vaccAIni = models.IntegerField(blank=True, null=True, verbose_name=explain("vaccAIni"))
    vaccARing = models.IntegerField(blank=True, null=True, verbose_name=explain("vaccARing"))
    vacnU = models.IntegerField(blank=True, null=True, verbose_name=explain("vacnU"))
    vacnUIni = models.IntegerField(blank=True, null=True, verbose_name=explain("vacnUIni"))
    vacnURing = models.IntegerField(blank=True, null=True, verbose_name=explain("vacnURing"))
    vacnA = models.IntegerField(blank=True, null=True, verbose_name=explain("vacnA"))
    vacnAIni = models.IntegerField(blank=True, null=True, verbose_name=explain("vacnAIni"))
    vacnARing = models.IntegerField(blank=True, null=True, verbose_name=explain("vacnARing"))
    vacwU = models.IntegerField(blank=True, null=True, verbose_name=explain("vacwU"))
    vacwUMax = models.IntegerField(blank=True, null=True, verbose_name=explain("vacwUMax"))
    vacwUMaxDay = models.IntegerField(blank=True, null=True, verbose_name=explain("vacwUMaxDay"))
    vacwUTimeMax = models.IntegerField(blank=True, null=True, verbose_name=explain("vacwUTimeMax"))
    vacwUTimeAvg = models.FloatField(blank=True, null=True, verbose_name=explain("vacwUTimeAvg"))
    vacwUDaysInQueue = models.IntegerField(blank=True, null=True, verbose_name=explain("vacwUDaysInQueue"))
    vacwA = models.FloatField(blank=True, null=True, verbose_name=explain("vacwA"))
    vacwAMax = models.FloatField(blank=True, null=True, verbose_name=explain("vacwAMax"))
    vacwAMaxDay = models.IntegerField(blank=True, null=True, verbose_name=explain("vacwAMaxDay"))
    vacwATimeMax = models.FloatField(blank=True, null=True, verbose_name=explain("vacwATimeMax"))
    vacwATimeAvg = models.FloatField(blank=True, null=True, verbose_name=explain("vacwATimeAvg"))
    vacwADaysInQueue = models.FloatField(blank=True, null=True, verbose_name=explain("vacwADaysInQueue"))


#####END DailyByProductionType######


class DailyByZoneAndProductionType(OutputBaseModel):
    iteration = models.IntegerField(blank=True, null=True, verbose_name=printable_name('iteration'),
        help_text='The iteration during which the outputs in this records where generated.', )
    day = models.IntegerField(blank=True, null=True, verbose_name=printable_name('day'),
        help_text='The day in this iteration during which the outputs in this records where generated.', )
    production_type = models.ForeignKey(ProductionType, blank=True, null=True, verbose_name=printable_name('production_type'),
        help_text='The identifier of the production type that these outputs apply to.', )
    last_day = models.BooleanField(default=False, help_text="Flag that is only set on the last day of an iteration.")
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
    last_day = models.BooleanField(default=False, help_text="Flag that is only set on the last day of an iteration.")
    zone = models.ForeignKey(Zone, blank=True, null=True, verbose_name=printable_name('zone'),
        help_text='The identifier of the zone that these outputs apply to.', )

    zoneArea          = models.FloatField(blank=True, null=True, verbose_name=printable_name('zoneArea'))
    zonePerimeter     = models.FloatField(blank=True, null=True, verbose_name=printable_name('zonePerimeter'))
    numSeparateAreas  = models.IntegerField(blank=True, null=True, verbose_name=printable_name('number of separate areas'))


class DailyControls(OutputBaseModel):
    iteration = models.IntegerField(blank=True, null=True, verbose_name=printable_name('iteration'),
        help_text='The iteration during which the outputs in this records where generated.', )
    day = models.IntegerField(blank=True, null=True, verbose_name=printable_name('day'),
        help_text='The day in this iteration during which the outputs in this records where generated.', )
    last_day = models.BooleanField(default=False, help_text="Flag that is only set on the last day of an iteration.")

    costSurveillance = models.FloatField(blank=True, null=True, verbose_name='Surveillance Cost')
    vaccSetup = models.FloatField(blank=True, null=True, verbose_name='Vaccination Site Setup Cost')
    vaccVaccination = models.FloatField(blank=True, null=True, verbose_name='Cost of Vaccine')
    vaccSubtotal = models.FloatField(blank=True, null=True, verbose_name='Vaccination Subtotal')
    destrAppraisal = models.FloatField(blank=True, null=True, verbose_name="Appraisal Cost")
    destrEuthanasia = models.FloatField(blank=True, null=True, verbose_name='Euthanasia Cost')
    destrIndemnification = models.FloatField(blank=True, null=True, verbose_name='Indemnification Cost')
    destrDisposal = models.FloatField(blank=True, null=True, verbose_name='Carcass Disposal Cost')
    destrCleaning = models.FloatField(blank=True, null=True, verbose_name='Cleaning and Disinfection Cost')
    destrSubtotal = models.FloatField(blank=True, null=True, verbose_name='Depopulation Subtotal Cost')
    costsTotal = models.FloatField(blank=True, null=True, verbose_name=printable_name('costsTotal'))

    deswUMax = models.IntegerField(blank=True, null=True, verbose_name="Destruction Wait Time Units Max")
    deswUMaxDay = models.IntegerField(blank=True, null=True, verbose_name="Destruction Wait Time Units Day with Max")
    deswUTimeMax = models.IntegerField(blank=True, null=True, verbose_name="Destruction Wait Time Units Max Time")
    deswUTimeAvg = models.FloatField(blank=True, null=True, verbose_name="Destruction Wait Time Units Average Time")
    deswUDaysInQueue = models.IntegerField(blank=True, null=True, verbose_name="Destruction Wait Time Units Days in Queue")
    deswAMax = models.IntegerField(blank=True, null=True, verbose_name="Destruction Wait Time Animals Max")
    deswAMaxDay = models.IntegerField(blank=True, null=True, verbose_name="Destruction Wait Time Animals Day with Max")
    deswATimeMax = models.IntegerField(blank=True, null=True, verbose_name="Destruction Wait Time Animals Max Time")
    deswATimeAvg = models.FloatField(blank=True, null=True, verbose_name="Destruction Wait Time Animals Average Time")
    deswADaysInQueue = models.IntegerField(blank=True, null=True, verbose_name="Destruction Wait Time Animals Days in Queue")
    vaccOccurred = models.IntegerField(blank=True, null=True, verbose_name='Vaccination Occurred')

    diseaseDuration = models.IntegerField(blank=True, null=True, verbose_name=printable_name('diseaseDuration'))
    outbreakDuration = models.IntegerField(blank=True, null=True, verbose_name=printable_name('outbreakDuration'))
    detOccurred = models.IntegerField(blank=True, null=True, verbose_name='Detection Occurred')
    destrOccurred = models.IntegerField(blank=True, null=True, verbose_name='Destruction Occurred')
    firstDetUInf = models.IntegerField(blank=True, null=True, verbose_name=printable_name('Units Infected at First Detection'))
    firstDetAInf = models.IntegerField(blank=True, null=True, verbose_name=printable_name('Animals Infected at First Detection'))
    detcUq = models.IntegerField(blank=True, null=True, verbose_name=printable_name('detcUq'))
    vaccTriggered = models.IntegerField(blank=True, null=True, verbose_name="First Vaccination Trigger Activated")


class UnitStats(OutputBaseModel):
    """Model for holding Unit related output primarily for the Results map Issue # 211.
    If we run into database contention issues, try switching the database mode to http://www.sqlite.org/draft/wal.html"""
    unit = models.OneToOneField(Unit,
        help_text='Pointer back to the input Unit (lat/long) these stats are for.')
    cumulative_infected = models.PositiveIntegerField(default=0,  # red
        help_text='The total number of iterations in which this unit became infected.', )
    cumulative_destroyed = models.PositiveIntegerField(default=0,  # black, larger circle laid behind up to 3x area
        help_text='The total number of iterations in which this unit was destroyed.', )
    cumulative_vaccinated = models.PositiveIntegerField(default=0,  # green
        help_text='The total number of iterations in which this unit was vaccinated.', )
    cumulative_zone_focus = models.PositiveIntegerField(default=0,  # blue, detection is the only zone trigger so this is "infected" related
        help_text='The total number of iterations in which this unit was a zone focus.', )


class ResultsVersion(OutputBaseModel):
    """There's a single copy of this model per set of output.  The version is grabbed from the first daily output from
    the C Engine.  All subsequent versions are discarded."""
    versionMajor = models.CharField(max_length=255, null=True, blank=True)
    versionMinor = models.CharField(max_length=255, null=True, blank=True)
    versionRelease = models.CharField(max_length=255, null=True, blank=True)
    
    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.id=1
        return super(ResultsVersion, self).save(force_insert, force_update, using, update_fields)

    def __str__(self):
        if all(x is not None for x in [self.versionMajor, self.versionMinor, self.versionRelease]):
            return '.'.join([self.versionMajor, self.versionMinor, self.versionRelease])
        else:
            return 'No simulation version stored in this result set'


def outputs_exist():
    return DailyControls.objects.count() > 0