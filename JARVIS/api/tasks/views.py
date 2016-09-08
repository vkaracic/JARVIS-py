"""API endpoint for listing tasks."""
from rest_framework.generics import ListCreateAPIView

from api.serializers import TaskSerializer
from queue.models import Task


class TaskListView(ListCreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
