from django.conf.urls import url

from api.twitter import views as twitter_views


urlpatterns = [
    url(r'^twitter/stream/', twitter_views.Stream.as_view()),
    url(r'^twitter/search/', twitter_views.Search.as_view()),
]
