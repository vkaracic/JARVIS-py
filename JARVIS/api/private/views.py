"""API endpoints for all TFModels."""
import json

from django.conf import settings
from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response

from api.serializers import TFModelSerializer
from users.models import ExtendedUser
from tf.models import TFModel
from queue.models import Task, Queue


def user_specific_qs(user):
    """Find the set of TF models that are:
      * Free use
      * Single use and the permitted user is the current user
      * Team use and the permitted team is the current user's team

    Args:
        user (auth.User): Current user

    Returns:
        Queryset of TF models that match the filter.
    """
    ext_user = ExtendedUser.objects.get(user=user)
    public = Q(permission_type=0)
    single_use = Q(permission_type=1, permitted_user=ext_user)
    team = Q(permission_type=2, permitted_team=ext_user.team)
    queryset = TFModel.objects.filter(
        public | single_use | team
    )
    return queryset


class PrivateModelListCreateView(ListCreateAPIView):
    """Private list and create endpoint.

    Methods:
        GET: Lists all the TFModels
        POST: Creates a new TFModel
    """
    serializer_class = TFModelSerializer

    def get_queryset(self):
        """Gets the querystring."""
        return user_specific_qs(self.request.user)

    def create(self, request, *args, **kwargs):
        """Creates a new TFModel. If the permission type is 1 (single_use),
        the request user is added as the permitted user, else if it's team use
        the current request user's team is added as the permitted team.
        """
        data = request.data
        if data['permission_type'] == 1:
            data['permitted_user'] = ExtendedUser.objects.get(user=request.user)
        elif data['permission_type'] == 2:
            data['permitted_team'] = request.user.team

        TFModel.objects.create(**data)

        return Response('Model created!')


class PrivateModelDetailsView(RetrieveUpdateDestroyAPIView, CreateAPIView):
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

    def get_queryset(self):
        """Gets the querystring."""
        return user_specific_qs(self.request.user)

    def post(self, request, pk):
        """Runs an inference with the TFModel and return the results."""
        model = TFModel.objects.get(id=pk, permission_type=0)
        # Must be list of lists
        input_data = request.data.get('input_data')
        inference = model.infer(input_data)
        return Response(inference)


class PrivateModelTrainView(APIView):
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

    def get_queryset(self):
        """Gets the querystring."""
        return user_specific_qs(self.request.user)

    def post(self, request, pk):
        """Runs the training of the TFModel."""
        err_data = request.data.get('min_error')
        iter_data = request.data.get('iterations')
        min_error = float(err_data) if err_data else None
        iterations = int(iter_data) if iter_data else 100000
        model = TFModel.objects.get(id=pk)
        ext_user = ExtendedUser.objects.get(user=request.user)

        if settings.QUEUE:
            training_data_csv_name = request.data.get('training_data_csv_name')
            Task.objects.create(
                model=model,
                priority=ext_user.priority,
                training_data_csv_name=training_data_csv_name,
                min_error=min_error,
                iterations=iterations
            )
            Queue.objects.first().start_next()
            return Response('Queued!')
        else:
            training_data = json.loads(request.data.get('training_data'))
            model.train(training_data, min_error, iterations)

        return Response('Trained!')
