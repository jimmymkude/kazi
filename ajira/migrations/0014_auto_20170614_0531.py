# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-14 05:31
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ajira', '0013_auto_20170614_0528'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='company',
            field=models.CharField(default='N/A', max_length=50),
        ),
    ]