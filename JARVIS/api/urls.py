from django.conf.urls import url
from rest_framework import routers

from api.twitter import views as twitter_views
from api.tf_api import views as tf_views
from api.queue_api import views as queue_views


urlpatterns = [
    url(r'^twitter/streaming/', twitter_views.Streaming.as_view()),
    url(r'^twitter/search/', twitter_views.Search.as_view()),
    url(r'^tf/models/$', tf_views.ModelListCreateView.as_view()),
    url(r'^tf/models/(?P<pk>[\d]+)/$', tf_views.ModelDetailsView.as_view()),
    url(r'^tf/models/(?P<pk>[\d]+)/train/$', tf_views.ModelTrainView.as_view()),
    url(r'^tasks/$', queue_views.TaskListView.as_view()),
]
