from __future__ import unicode_literals

import csv
from datetime import datetime
from os import path
import pytz
import time

from django.conf import settings
from django.db import models


class Queue(models.Model):
    timeout = models.PositiveIntegerField(default=0)
    pause = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        """ Singleton class. """
        self.id = 1
        super(Queue, self).save(*args, **kwargs)
        if not self.pause:
            self.start_next()

    def delete(self, *args, **kwargs):
        pass

    def _start(self, next_task):
        next_task.start()
        if self.timeout:
            time.sleep(self.timeout)
        self.start_next()

    def start_next(self):
        if not self.pause:
            # If the last three tasks errored then there is a bigger problem
            # and the execution should not continue.
            last_statuses = Task.objects.all().reverse()[:3].values_list(
                'status', flat=True
            )
            if sum(last_statuses) == 9:
                return False
            next_task = Task.objects.filter(status=0).first()
            if not Task.objects.filter(status=1).exists() and next_task:
                self._start(next_task)


class Task(models.Model):
    STATUS_CHOICES = (
        (0, 'WAITING'),
        (1, 'RUNNING'),
        (2, 'DONE'),
        (3, 'ERROR'),
    )
    priority = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    started_at = models.DateTimeField(null=True, blank=True)
    finished_at = models.DateTimeField(null=True, blank=True)
    model = models.ForeignKey('tf.TFModel')
    training_data_csv_name = models.CharField(max_length=255, blank=True, null=True)
    min_error = models.FloatField(null=True, blank=True)
    iterations = models.PositiveIntegerField(null=True, blank=True)
    status = models.IntegerField(default=0, choices=STATUS_CHOICES)
    error = models.TextField()

    class Meta(object):
        ordering = ['created_at', 'priority']

    def __str__(self):
        return '{}, status: {}'.format(self.id, self.status)

    def load_training_data_csv(self):
        file_path = path.join(
            settings.BASE_DIR,
            'training_datasets/{}'.format(self.training_data_csv_name)
        )
        with open(file_path, 'r') as f:
            data = []
            for row in csv.reader(f):
                input_data = map(float, row[:self.model.num_inputs])
                output_data = map(float, row[self.model.num_inputs:])
                data.append([input_data, output_data])
        return data

    def start(self):
        self.started_at = pytz.utc.localize(datetime.now())
        training_data = self.load_training_data_csv()
        self.status = 1
        self.save()
        try:
            self.model.train(training_data, self.min_error, self.iterations)
            self.status = 2
        except Exception as ex:
            self.error = ex
            self.status = 3
            self.save()
        self.finished_at = pytz.utc.localize(datetime.now())
        self.save()
        if self.status == 2:
            print 'Task [%s] finished in [%s]!' % (
                self.id,
                self.finished_at - self.started_at
            )
        else:
            print 'Task [%s] failed!', self.id

        Queue.objects.first().start_next()
