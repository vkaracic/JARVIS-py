import json

from rest_framework.decorators import detail_route
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response

from api.serializers import TFModelSerializer
from tf.models import TFModel


class ModelListCreateView(ListCreateAPIView):
    queryset = TFModel.objects.all()
    serializer_class = TFModelSerializer


class ModelDetailsView(RetrieveUpdateDestroyAPIView, CreateAPIView):
    serializer_class = TFModelSerializer
    queryset = TFModel.objects.all()

    def post(self, request, pk):
        model = TFModel.objects.get(id=pk)
        # Must be list of lists
        predict_data = json.loads(request.POST.get('predict_data'))
        prediction = model.predict(predict_data)
        return Response(prediction)


class ModelTrainView(APIView):
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
