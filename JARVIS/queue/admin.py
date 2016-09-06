from django.contrib import admin

from queue.models import Task, Queue

admin.site.register(Task)
admin.site.register(Queue)
