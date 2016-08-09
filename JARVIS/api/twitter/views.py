import csv
from datetime import datetime
import json
import re

from django.conf import settings
from tweepy import API
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.parsers import JSONParser
from tweepy.streaming import StreamListener
from rest_framework.status import HTTP_400_BAD_REQUEST
from rest_framework.response import Response
from rest_framework.views import APIView

CKEY = settings.TWITTER_CONSUMER_KEY
CSECRET = settings.TWITTER_CONSUMER_SECRET
ATOKEN = settings.TWITTER_ACCESS_TOKEN
ASECRET = settings.TWITTER_ACCESS_TOKEN_SECRET


def twitter_auth():
    """ Twitter authentication via Tweepy. """
    auth = OAuthHandler(CKEY, CSECRET)
    auth.set_access_token(ATOKEN, ASECRET)
    return auth


def parse_tweet(string):
    """
    Ignore special, non-ascii characters in tweets. 
    Remove retweets and URL links.
    """
    ascii_filtered = unicode(string).encode('ascii', 'ignore')
    rt_p = re.compile(r'@[\w\d]+:?')
    url_p = re.compile(r'http[s]?:\/\/[\w\d\.\-_\/]+')
    no_rt = re.sub(rt_p, '', ascii_filtered)
    no_url = re.sub(url_p, '', no_rt)
    return no_url.replace('RT', '')


def save_to_csv(filename, data):
    """
    Writes tweets to a CSV.
    The delimiter is tab because commas are common in tweets.
    """
    with open(filename, 'wb') as csvfile:
        writer = csv.DictWriter(
            csvfile, fieldnames=['user', 'tweet'], delimiter='\t'
        )
        writer.writeheader()
        for item in data:
            try:
                writer.writerow(item)
            except BaseException as e:
                print "ERROR: ", e


class Listener(StreamListener):
    """
    Twitter listener.
    Classifies most common Twitter messages and routes to appropriately
    named methods.
    """
    def __init__(self, keyword, limit):
        self.keyword = keyword
        self.limit = limit
        self.count = 0
        self.collection = []

    def on_data(self, data):
        """
        Controlling the retrieved data.
        Receives the amount of tweets that it is limited to and writes them in
        a CSV file named "stream_<keyword>_<datetime>.csv".
        """
        self.count += 1
        if self.count > int(self.limit):
            filename = 'stream_{}_{}.csv'.format(
                self.keyword, datetime.now().isoformat()
            )
            save_to_csv(filename, self.collection)
            return False

        json_data = json.loads(data)
        # Ignore non-ascii codes in tweets.
        data = {
            'user': parse_tweet(json_data['user']['name']),
            'tweet': parse_tweet(json_data['text'])
        }
        self.collection.append(data)
        return True

    def on_error(self, status):
        """ Error handler. """
        print status


class Streaming(APIView):
    """ API endpoint for retrieving data from Twitter stream. """

    def get(self, request, *args, **kwargs):
        """
        The GET method controller for the API endpoint.
        Accepts query strings:
            - keyword: the keyword that is looked for in tweets
            - limit: the limit of tweets that are fetched
        """
        keyword = request.GET.get('keyword')
        limit = request.GET.get('limit')

        # Establishes a streaming session and routes messages
        # to Listener instance.
        auth = twitter_auth()

        twitter_stream = Stream(auth, Listener(keyword, limit))
        twitter_stream.filter(track=[keyword])

        return Response()


class Search(APIView):
    """ API endpoint for retrieving data from Twitter search. """

    def get(self, request, *args, **kwargs):
        """
        The GET method controller for the API endpoint and saves the results
        to a CSV file.
        Accepts query strings:
            - keyword: the keyword that searched for
            - count: number of results retrieved (default = 100)
        """
        keyword = request.GET.get('keyword')
        count = request.GET.get('count', 100)
        if not keyword:
            return Response(HTTP_400_BAD_REQUEST)

        auth = twitter_auth()
        api = API(auth, parser=JSONParser())
        data = []
        results = api.search(q=keyword, count=count)
        filename = 'search_{}_{}.csv'.format(
            keyword, datetime.now().isoformat()
        )
        for result in results['statuses']:
            data.append({
                'user': parse_tweet(result['user']['name']),
                'tweet': parse_tweet(result['text'])
            })
        save_to_csv(filename, data)
        response_text = 'Saved {} objects.'.format(
            results['search_metadata']['count']
        )
        return Response(response_text)
