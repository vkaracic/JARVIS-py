from django.conf.urls import url

from jsapp.views import MlpView, LstmView


urlpatterns = [
    url(r'^mlp$', MlpView.as_view(), name='mlp'),
    url(r'^lstm$', LstmView.as_view(), name='lstm'),
]
