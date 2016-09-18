# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-09-18 16:20
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tf', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='tfmodel',
            name='title',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='tfmodel',
            name='external_id',
            field=models.CharField(max_length=8, unique=True),
        ),
    ]