# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-19 12:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ajira', '0018_careerinterests_job_types'),
    ]

    operations = [
        migrations.AddField(
            model_name='jobtitle',
            name='title_lower',
            field=models.CharField(default='n/a', max_length=60),
        ),
        migrations.AddField(
            model_name='post',
            name='title_lower',
            field=models.CharField(default='n/a', max_length=60),
        ),
    ]
