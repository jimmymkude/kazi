# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-12 19:03
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ajira', '0008_auto_20170611_0643'),
    ]

    operations = [
        migrations.AddField(
            model_name='ajirauser',
            name='company_name',
            field=models.CharField(default='N/A', max_length=50),
        ),
        migrations.AddField(
            model_name='ajirauser',
            name='job_title',
            field=models.CharField(default='N/A', max_length=50),
        ),
    ]
