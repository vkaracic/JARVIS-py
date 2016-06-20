from django.conf.urls import url

from api.twitter import views as twitter_views
from api.instagram import views as instagram_views


urlpatterns = [
    url(r'^twitter/streaming/', twitter_views.Streaming.as_view()),
    url(r'^twitter/search/', twitter_views.Search.as_view()),
    url(r'^instagram/search/', instagram_views.Search.as_view()),
    url(r'^instagram/token/', instagram_views.Token.as_view()),
]
