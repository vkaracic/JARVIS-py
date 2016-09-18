"""Serializers for model data."""
from rest_framework import serializers

from tf.models import TFModel, TrainingResults
from queue.models import Task


class TFModelSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = TFModel
        exclude = ('file_path', )


class TaskSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = Task


class ResultsSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = TrainingResults
