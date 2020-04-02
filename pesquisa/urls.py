from django.conf.urls import url
from . import views
from django.urls import path, include
from django.views.generic import TemplateView
#
# Created on Tue Mar 31 2020
#
# Copyright (c) 2020 Maurício André Kunz
# mauricioandrek@hotmail.com
#


urlpatterns = [
    url(r'^$', views.index, name='home'),
    url(r'^leitura/', views.leitura, name='leitura'),
    url(r'^administrador', views.administrador, name='administrador'),
    url(r'^ar/', TemplateView.as_view(template_name="pesquisa/ar.html"),
                   name='ar'),
]