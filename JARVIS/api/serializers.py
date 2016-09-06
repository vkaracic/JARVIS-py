from rest_framework import serializers

from tf.models import TFModel
from queue.models import Task


class TFModelSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = TFModel
        exclude = ('file_path', )


class TaskSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = Task
