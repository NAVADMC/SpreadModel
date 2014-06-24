from django.db import models
from ScenarioCreator.models import ProductionType, Zone, Unit
import re

"""Results models explanation: The Results models are containers to capture all of the output generated by the CEngine
simulation and present it to the user broken down into 13 different tables.

Model Declarations: Each model creates a table in sqlite3 and a 'model' for table presentation on the GUI.  So
 each model serves double duty.  Notice that there are effectively 3 names for each field inside a model.
 1) the Python name (e.g. tsdASusc = models.) is used when constructing the object and is designed to match the CEngine output.
 2) the db_column name will show up when a user exports the DataBase.  They are at least readable explanations.
 3) verbose_name is used in the GUI for displaying Table headers.  Without this, Django would use the Python name,
 which is significantly more obscure.
 The code in scripts/Output_Table.py (.ipynb) was used to generate these name declarations.  Also, if you're reading this
 doc and you don't know about IPython Notebooks, go get IPython Notebooks."""


def create_from_line(line):
    pass


class OutputManager(models.Manager):
    def bulk_create(self, header_line, cmd_strings, *args, **kwargs):
        headers = header_line.split(',')
        report_objects = []
        for cmd_string in cmd_strings:
            sparse_values = {}
            values = cmd_string.split(',')
            pairs = zip(headers, values)
            for key, value in pairs:
                if value and value != '0':
                    sparse_values[key] = int(value)
            report_objects.append(DailyReport(sparse_dict=str(sparse_values)))

        # for obj in report_objects:
        #     print(obj)  #.save()
        return super().bulk_create(report_objects)


class DailyReport(models.Model):
    sparse_dict = models.TextField()
    # to get the dictionary object back:
    # import ast
    # ast.literal_eval("{'muffin' : 'lolz', 'foo' : 'kitty'}")

    objects = OutputManager()

    def __str__(self):
        return self.sparse_dict


def printable_name(underscores_name):
    spaced = re.sub(r'_', r' ', underscores_name)
    return spaced.title()  # capitalize


class DailyByProductionType(models.Model):
    iteration = models.IntegerField(blank=True, null=True, db_column='iteration', verbose_name=printable_name('iteration'),
        help_text='The iteration during which the outputs in this records where generated.', )
    production_type = models.ForeignKey(ProductionType,
        help_text='The identifier of the production type that these outputs apply to.', )

class DailyByZoneAndProductionType(models.Model):
    pass

class DailyByZone(models.Model):
    pass


class DailyControls(models.Model):
    pass