import csv
import datetime
import json

from django.conf import settings
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
from rest_framework.views import APIView
from rest_framework.response import Response

CKEY = settings.TWITTER_CONSUMER_KEY
CSECRET = settings.TWITTER_CONSUMER_SECRET
ATOKEN = settings.TWITTER_ACCESS_TOKEN
ASECRET = settings.TWITTER_ACCESS_TOKEN_SECRET


class Listener(StreamListener):
    """
    Twitter listener.
    Classifies most common Twitter messages and routes to appropriately named methods.
    """
    def __init__(self, keyword, limit, api=None):
        super(Listener, self).__init__(api=api)
        self.keyword = keyword
        self.limit = limit
        self.count = 0
        self.collection = []

    def on_data(self, data):
        """
        Controlling the retrieved data.
        Receives the amount of tweets that it is limited to and writes them in
        a CSV file named "<keyword>_<datetime>.csv". The delimiter is tab because
        commas are common in tweets.
        """
        self.count += 1
        if self.count > int(self.limit):
            filename = '{}_{}.csv'.format(self.keyword, datetime.datetime.now().isoformat())
            with open(filename, 'wb') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=['user', 'tweet'], delimiter='\t')
                writer.writeheader()
                for data in self.collection:
                    try:
                        writer.writerow(data)
                    except BaseException as e:
                        print "ERROR: ", e
            return False

        json_data = json.loads(data)
        # Ignore non-ascii codes in tweets.
        data = {
            'user': unicode(json_data['user']['name']).encode('ascii', 'ignore'),
            'tweet': unicode(json_data['text']).encode('ascii', 'ignore')
        }
        self.collection.append(data)
        return True

    def on_error(self, status):
        """ Error handler. """
        print status


class TwitterStream(APIView):
    """ API endpoint for retrieving data from Twitter. """

    def get(self, request, *args, **kwargs):
        """
        The GET method controller for the API endpoint.
        Accepts query strings:
            - keyword: the keyword that is looked for in tweets
            - limit: the limit of tweets that are fetched
        """
        keyword = request.GET.get('keyword')
        limit = request.GET.get('limit')

        auth = OAuthHandler(CKEY, CSECRET)
        auth.set_access_token(ATOKEN, ASECRET)

        # Establishes a streaming session and routes messages to Listener instance.
        twitter_stream = Stream(auth, Listener(keyword, limit))
        twitter_stream.keyword(track=[keyword])

        return Response()
