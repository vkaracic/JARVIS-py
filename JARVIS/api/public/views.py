"""API endpoints for free use TFModels."""
import json

from django.conf import settings
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response

from api.serializers import TFModelSerializer
from tf.models import TFModel
from queue.models import Task, Queue


class ModelListCreateView(ListCreateAPIView):
    """TFModel list endpoint.

    Methods:
        GET: Lists all the TFModels which are free use
        POST: Creates a new free use TFModel
    """
    queryset = TFModel.objects.filter(permission_type=0)
    serializer_class = TFModelSerializer


class ModelDetailsView(RetrieveUpdateDestroyAPIView, CreateAPIView):
    """Endpoint for individual TFModels.

    Methods:
        GET: Show the details of the TFModel.
        POST: Run an inference with the TFModel.
            args:
                - input_data: List of lists containing input values for
                    the model
        PUT: Update the complete TFModel.
        PATCH: Partically update the TFModel.
        DELETE: Delete the TFModel.
    """
    serializer_class = TFModelSerializer
    queryset = TFModel.objects.filter(permission_type=0)

    def post(self, request, pk):
        """Runs an inference with the TFModel and return the results."""
        model = TFModel.objects.get(id=pk, permission_type=0)
        # Must be list of lists
        input_data = json.loads(request.POST.get('input_data'))
        inference = model.infer(input_data)
        return Response(inference)


class ModelTrainView(APIView):
    """Endpoint for training a TFModel.

    Methods:
        POST: Runs the training of the TFModel.
            args:
                - training_data (list): List of inputs matched with the target outputs.
                    For example XOR training data would look like:
                        [[[0, 0],[0]],[[0, 1],[1]],[[1, 0],[1]],[[1, 1],[0]]]
                - training_data_csv_name: Name of training dataset file.
                - min_error (float): Minimum error.
                - iterations (int): Number of iterations.
    """
    serializer_class = TFModelSerializer
    queryset = TFModel.objects.filter(permission_type=0)

    def post(self, request, pk):
        """Runs the training of the TFModel."""
        err_data = request.POST.get('min_error')
        iter_data = request.POST.get('iterations')
        min_error = float(err_data) if err_data else None
        iterations = int(iter_data) if iter_data else 100000
        training_data_csv_name = request.POST.get('training_data_csv_name')
        model = TFModel.objects.get(id=pk, permission_type=0)

        if settings.QUEUE:
            Task.objects.create(
                model=model,
                training_data_csv_name=training_data_csv_name,
                min_error=min_error,
                iterations=iterations
            )
            Queue.objects.first().start_next()
            return Response('Queued!')
        else:
            training_data = json.loads(request.POST.get('training_data'))
            model.train(training_data, min_error, iterations)

        return Response('Trained!')
