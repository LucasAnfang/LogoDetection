# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-10-17 22:57
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('detector', '0003_trainingupload'),
    ]

    operations = [
        migrations.AddField(
            model_name='trainingupload',
            name='brand',
            field=models.CharField(default='NULL', max_length=50),
            preserve_default=False,
        ),
    ]
