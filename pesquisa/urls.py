from django.conf.urls import url
from . import views
from django.urls import path, include

urlpatterns = [
    url(r'^$', views.index, name='home'),
    url(r'^leitura/', views.leitura, name='leitura'),
    url(r'^administrador', views.administrador, name='administrador'),
]