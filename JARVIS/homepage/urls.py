from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from homepage.views import Index, Register


urlpatterns = [
    url(r'^register/$', Register.as_view(), name='register'),
    url(r'^$', login_required(Index.as_view()), name='index'),
]
