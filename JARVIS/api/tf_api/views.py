import json

from rest_framework.decorators import detail_route
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response

from api.serializers import TFModelSerializer
from tf.models import TFModel


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
        POST: Run a prediction with the TFModel.
            args:
                - predict_data: List of lists containing input values for
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
        predict_data = json.loads(request.POST.get('predict_data'))
        prediction = model.predict(predict_data)
        return Response(prediction)


class ModelTrainView(APIView):
    """Endpoint for training a TFModel.

    Methods:
        POST: Runs the training of the TFModel.
            args:
                - training_data (list): List of inputs matched with the target outputs.
                    For example XOR training data would look like:
                        [[[0, 0],[0]],[[0, 1],[1]],[[1, 0],[1]],[[1, 1],[0]]]
                - min_error (float): Minimum error.
                - iterations (int): Number of iterations.
    """
    serializer_class = TFModelSerializer
    queryset = TFModel.objects.all()

    def post(self, request, pk):
        training_data = json.loads(request.POST.get('training_data'))
        err_data = request.POST.get('min_error')
        iter_data = request.POST.get('iterations')

        min_error = float(err_data) if err_data else None
        iterations = float(iter_data) if iter_data else 100000

        model = TFModel.objects.get(id=pk)
        model.train(training_data, min_error, iterations)

        return Response('Trained!')
