from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from api.twitter import views as twitter_views
from api.public import views as public_views
from api.tasks import views as task_views
from api.private import views as private_views
from api.results import views as result_views


urlpatterns = [
    url(r'^twitter/streaming/', twitter_views.Streaming.as_view()),
    url(r'^twitter/search/', twitter_views.Search.as_view()),
    url(r'^public/models/$', public_views.ModelListCreateView.as_view()),
    url(r'^public/models/(?P<pk>[\d]+)/$', public_views.ModelDetailsView.as_view()),
    url(r'^public/models/(?P<pk>[\d]+)/train/$', public_views.ModelTrainView.as_view()),
    url(r'^tasks/$', task_views.TaskListView.as_view()),
    url(r'^private/models/$', login_required(private_views.PrivateModelListCreateView.as_view())),
    url(r'^private/models/(?P<pk>[\d]+)/$', login_required(private_views.PrivateModelDetailsView.as_view())),
    url(r'^private/models/(?P<pk>[\d]+)/train/$', login_required(private_views.PrivateModelTrainView.as_view())),
    url(r'^results/(?P<exid>[\w]+)/$', result_views.ResultsView.as_view())
]
