# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-10 21:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=50)),
                ('middle_initial', models.CharField(max_length=1)),
                ('last_name', models.CharField(max_length=50)),
            ],
        ),
    ]
