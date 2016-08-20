# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-08-20 21:17
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models
import re
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TFModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('external_id', models.UUIDField(default=uuid.uuid4, unique=True)),
                ('file_path', models.FilePathField(blank=True, null=True)),
                ('num_inputs', models.PositiveIntegerField()),
                ('num_outputs', models.PositiveIntegerField()),
                ('num_hidden', models.CharField(max_length=255, validators=[django.core.validators.RegexValidator(re.compile('^\\d+(?:\\,\\d+)*\\Z'), code='invalid', message='Enter only digits separated by commas.')])),
                ('learning_rate', models.FloatField()),
                ('cost', models.CharField(max_length=255)),
                ('optimizer', models.CharField(max_length=255)),
                ('activation', models.CharField(max_length=255)),
                ('trained', models.BooleanField(default=False)),
            ],
        ),
    ]