from django.shortcuts import render
from django.views.generic.base import TemplateView


class MlpView(TemplateView):
    template_name = 'mlp.html'


class LstmView(TemplateView):
    template_name = 'lstm.html'
