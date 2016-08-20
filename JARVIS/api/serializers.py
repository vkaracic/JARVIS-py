from rest_framework import serializers

from tf.models import TFModel


class TFModelSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = TFModel
        exclude = ('file_path', )
