# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-14 05:34
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ajira', '0015_auto_20170614_0532'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ajirauser',
            name='company_name',
            field=models.CharField(default='N/A', max_length=30),
        ),
        migrations.AlterField(
            model_name='post',
            name='company',
            field=models.CharField(default='N/A', max_length=30),
        ),
        migrations.AlterField(
            model_name='post',
            name='title',
            field=models.CharField(max_length=60),
        ),
    ]
