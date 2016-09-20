from rest_framework.views import APIView
from rest_framework.response import Response

from api.serializers import ResultsSerializer
from tf.models import TrainingResults


class ResultsView(APIView):
    serializer = ResultsSerializer

    def get(self, request, exid, *args, **kwargs):
        try:
            results = TrainingResults.objects.get(model=exid)
            return Response(ResultsSerializer(results).data)
        except TrainingResults.DoesNotExist:
            return Response({})
