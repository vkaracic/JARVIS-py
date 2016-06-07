from django.conf import settings
from instagram.client import InstagramAPI
from rest_framework.status import HTTP_400_BAD_REQUEST
from rest_framework.response import Response
from rest_framework.views import APIView
import requests


class Token(APIView):
    def get(self, request, *args, **kwargs):
        url = 'https://api.instagram.com/oauth/authorize/?client_id={}&redirect_uri={}&response_type=token&scope=public_content'.format(
            settings.INSTAGRAM_CLIENT_ID, 'http%3A%2F%2Fvedrankaracic.com%2F'
        )
        return Response(url)


class Search(APIView):
    def get(self, request, *args, **kwargs):
        keyword = request.GET.get('keyword')
        access_token = request.GET.get('access_token')
        if not keyword and not access_token:
            return Response(HTTP_400_BAD_REQUEST)

        response = requests.get('https://api.instagram.com/v1/tags/{}/media/recent?access_token={}'.format(keyword, access_token))
        return Response(response.content)
