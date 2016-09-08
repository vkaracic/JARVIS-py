# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-09-08 07:34
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('tf', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Queue',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timeout', models.PositiveIntegerField(default=0)),
                ('pause', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('priority', models.IntegerField(default=1)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('started_at', models.DateTimeField(blank=True, null=True)),
                ('finished_at', models.DateTimeField(blank=True, null=True)),
                ('training_data_csv_name', models.CharField(blank=True, max_length=255, null=True)),
                ('min_error', models.FloatField(blank=True, null=True)),
                ('iterations', models.PositiveIntegerField(blank=True, null=True)),
                ('status', models.IntegerField(choices=[(0, 'WAITING'), (1, 'RUNNING'), (2, 'DONE'), (3, 'ERROR')], default=0)),
                ('error', models.TextField()),
                ('model', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tf.TFModel')),
            ],
            options={
                'ordering': ['created_at', 'priority'],
            },
        ),
    ]
