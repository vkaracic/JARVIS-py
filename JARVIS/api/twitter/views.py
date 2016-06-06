import json

from django.conf import settings
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
from rest_framework.views import APIView

CKEY = settings.TWITTER_CONSUMER_KEY
CSECRET = settings.TWITTER_CONSUMER_SECRET
ATOKEN = settings.TWITTER_ACCESS_TOKEN
ASECRET = settings.TWITTER_ACCESS_TOKEN_SECRET


class Listener(StreamListener):
    """
    Twitter listener.
    Classifies most common Twitter messages and routes to appropriately named methods.
    """

    def on_data(self, data):
        """
        Controlling the retrieved data.
        Receives all messages and calls functions according to the message type.
        """
        json_data = json.loads(data)
        print "User: ", unicode(json_data['user']['name'])
        print "Tweet: ", unicode(json_data['text'])
        return True

    def on_error(self, status):
        """ Error handler. """
        print status


class FetchTweets(APIView):
    """ API endpoint for retrieving data from Twitter. """

    def get(self, request, *args, **kwargs):
        hashtag = request.GET.get('hashtag')

        auth = OAuthHandler(CKEY, CSECRET)
        auth.set_access_token(ATOKEN, ASECRET)

        # Establishes a streaming session and routes messages to Listener instance.
        twitter_stream = Stream(auth, Listener())
        twitter_stream.filter(track=["SpaceX"])
