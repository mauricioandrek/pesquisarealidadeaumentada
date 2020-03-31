from django.shortcuts import render, redirect, get_object_or_404
from django.core.files.storage import FileSystemStorage, default_storage
from django.http import HttpResponse
from django import template
from .models import Manifest
import csv, io
from django.utils import timezone
import uuid
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)

# Create your views here.
def index(request):
    return render(request, 'pesquisa/index.html', {})

def leitura(request):
	return render(request, 'pesquisa/leitura.html', {})

def administrador(request):
	global logger
	dados = Manifest.objects.all()
	logger.error("dados : {0}".format(dados))  
	template = 'pesquisa/admin.html'
	if request.method == "GET":
		return render(request, template, { 'manifestos': dados })
	        
	csv_file = request.FILES['myfile']
    # checar se é um CSV
	if not csv_file.name.endswith('.csv'):
		messages.error(request, 'Não foi selecionado um arquivo CSV')
		
	data_set = csv_file.read().decode('UTF-8')
	io_string = io.StringIO(data_set)
	next(io_string)
	Manifest.objects.all().delete()
	for column in csv.reader(io_string, delimiter=',', quotechar="|"):
		_, created = Manifest.objects.update_or_create(
			step=column[0],
			typee=column[1],
			value=column[2],
			desc=column[3],
			imported_date = timezone.now()
			)
	dados = Manifest.objects.all()
	return render(request, template, {'manifestos' : dados })