from django.conf.urls import url

from api.twitter import views as twitter_views


urlpatterns = [
    url(r'^twitter/fetch_tweets/', twitter_views.FetchTweets.as_view()),
]
