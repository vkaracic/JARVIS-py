from django.conf.urls import url

from homepage.views import Index


urlpatterns = [
    url(r'^$', Index.as_view(), name='index'),
]
