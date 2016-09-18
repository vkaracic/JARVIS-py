from django.contrib import admin

from tf.models import TFModel, TrainingResults


admin.site.register(TFModel)
admin.site.register(TrainingResults)
