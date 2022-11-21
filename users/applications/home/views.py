import datetime
from sys import implementation
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin


class FechaMixin(object):

    def get_context_data(self, **kwargs):
        context = super(FechaMixin, self).get_context_data(**kwargs)
        context['fecha']= datetime.datetime.now()
        return context


class HomePage(LoginRequiredMixin, TemplateView):
    template_name = "home/index.html"
    #si el usuario no esta logueado
    login_url= reverse_lazy('users_app:user-login')
# Create your views here.




class TemplatePruebaMixin(FechaMixin, TemplateView):
    template_name = "home/mixin.html"
