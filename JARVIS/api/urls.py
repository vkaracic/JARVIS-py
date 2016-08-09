from django.conf.urls import url

from api.twitter import views as twitter_views


urlpatterns = [
    url(r'^twitter/streaming/', twitter_views.Streaming.as_view()),
    url(r'^twitter/search/', twitter_views.Search.as_view()),
]
