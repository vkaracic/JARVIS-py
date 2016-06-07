from django.conf.urls import url

from api.twitter import views as twitter_views


urlpatterns = [
    url(r'^twitter/stream/', twitter_views.TwitterStream.as_view()),
]
