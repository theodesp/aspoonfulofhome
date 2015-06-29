# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_standardpage_standardpagerelatedlink'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogindexpage',
            name='intro',
            field=models.CharField(help_text='Intro', max_length=255),
        ),
        migrations.AlterField(
            model_name='standardpage',
            name='intro',
            field=models.CharField(help_text='Intro', max_length=255),
        ),
    ]
