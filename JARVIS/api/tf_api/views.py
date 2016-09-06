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
        GET: Lists all the TFModels
        POST: Creates a new TFModel
    """
    queryset = TFModel.objects.all()
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
    queryset = TFModel.objects.all()

    def post(self, request, pk):
        model = TFModel.objects.get(id=pk)
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
                - training_data_csv_name: Name of training dataset file. Used for queued training.
                - min_error (float): Minimum error.
                - iterations (int): Number of iterations.
    """
    serializer_class = TFModelSerializer
    queryset = TFModel.objects.all()

    def post(self, request, pk):
        err_data = request.POST.get('min_error')
        iter_data = request.POST.get('iterations')
        min_error = float(err_data) if err_data else None
        iterations = int(iter_data) if iter_data else 100000
        model = TFModel.objects.get(id=pk)

        if settings.QUEUE:
            training_data_csv_name = request.POST.get('training_data_csv_name')
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
