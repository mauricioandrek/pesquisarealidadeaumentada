from django.shortcuts import render, redirect, get_object_or_404
from django.core.files.storage import FileSystemStorage, default_storage
from django.http import HttpResponse
from django import template
import uuid

# Create your views here.
def index(request):
    return render(request, 'pesquisa/index.html', {})

def leitura(request):
	return render(request, 'pesquisa/leitura.html', {})

def administrador(request):
	return render(request, 'pesquisa/admin.html', {})