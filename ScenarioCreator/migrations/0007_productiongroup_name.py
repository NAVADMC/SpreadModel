# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ScenarioCreator', '0006_vacc_triggers_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='productiongroup',
            name='name',
            field=models.CharField(default='All', max_length=255),
            preserve_default=False,
        ),
    ]
