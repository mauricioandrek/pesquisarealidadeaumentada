from django.shortcuts import render, redirect, get_object_or_404
import json
from django.core.files.storage import FileSystemStorage, default_storage
from django.db.models import Count
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django import template
from .models import Manifest
from .utils import Utils
from .other_models import State, Option
import csv, io
from django.utils import timezone
from django.contrib import messages
import uuid
import logging
#
# Created on Tue Mar 31 2020
#
# Copyright (c) 2020 Maurício André Kunz
# mauricioandrek@hotmail.com
#

logger = logging.getLogger(__name__)
def carregarSessao(request):
	state_zero = State('', '','','','', [])
	states = []
	states_final = []
	#region Carregamento do Array de Estados [states, state_zero, states_final]
	try:
		steps = Manifest.objects.values('step').annotate(dcount=Count('step'))
		jaBuscouResultados = None
		for step_item in steps:
			if (step_item['step'] == '0'):
				try:
					manifest0 = Manifest.objects.get(step = step_item['step'])
					state_zero = State('', '','','','', [])
					state_zero.name = manifest0.value
					state_zero.desc = manifest0.desc
				except Manifest.DoesNotExist:
					logger.error("Manifesto 0 não existe, definindo atividade padrão")
					state_zero = State('', '','','','', [])
					state_zero.name = Utils.NOME_APLICACAO()
					state_zero.desc = Utils.DESCRICAO_APLICACAO()
				continue
			elif(not jaBuscouResultados and step_item['step'] == 'F'):
				try:
					jaBuscouResultados = True
					manifests = Manifest.objects.filter(step = step_item['step'])
					for manifest in manifests:
						state_final = State('', '','','','', [])
						state_final.step = step_item['step']
						if(manifest.typee == 'result'):
							state_final.name = manifest.value
							state_final.desc = manifest.desc	
						states_final.append(state_final)
				except Manifest.DoesNotExist:
					logging.exception("Erro ao definir estados finais")
				continue
			manifests = Manifest.objects.filter(step = step_item['step'])
			state = State('', '','','','', [])
			state.step = step_item['step']
			for manifest in manifests:
				if(manifest.typee == 'model'):
					state.model = manifest.value
				elif(manifest.typee == 'marker'):
					state.marker = manifest.value
				elif(manifest.typee == 'op'):
					option = Option()
					option.step = step_item['step']
					option.value = manifest.value
					option.desc = manifest.desc
					state.options.append(option)
				elif(manifest.typee == 'info'):
					state.name = manifest.value
					state.desc = manifest.desc	
			states.append(state)
	except Exception as e:
		logging.exception("Erro ao carregar array de estados")
	#endregion Carregamento do Array de Estados [states, state_zero, states_final]
	# for state in states:
	# 	logger.error("state : {0}".format(state))
	# for state in states_final:
	# 	logger.error("statefinal : {0}".format(state))
	# armazena na sessão os estados e atualiza o timeout 
	try:
		request.session['state_zero'] = Utils.ObjectToJson(state_zero)
		request.session['states'] = Utils.ObjectToJson(states)
		request.session['states_final'] = Utils.ObjectToJson(states_final)
		request.session.set_expiry(3600)
	except Exception as e:
		logging.exception("Erro armazenar dados da sessão")
	return True

def index(request):
	global logger
	request.session.set_expiry(3600)
	if carregarSessao(request):
		state_zero = State.JsonToModel(request.session['state_zero'])	

	if(request.session.get('states')):
		states = State.JsonToModelArray(request.session['states'])
		states.sort(key=lambda x: x.step, reverse=False)
	
	if request.method == "POST":
		if request.session.get('results'):
			del request.session['results']
		if(len(states) > 0):
			state_now = states[0]
			request.session['state_now'] = Utils.ObjectToJson(state_now)
		else:
			if request.session.get('state_now'):
				del request.session['state_now']
		if request.session.get('concluido'):
			del request.session['concluido']
			
		return HttpResponseRedirect('/')

	if(request.session.get('state_now')):
		state_now = State.JsonToModel(request.session['state_now'])
	concluido = False
	if(request.session.get('concluido')):
		if request.session['concluido']:
			concluido = True

	return render(request, 'pesquisa/index.html', { 'state_zero': state_zero, 'concluido' : concluido })

def leitura(request):
	states = None
	states_final = None
	state_now = State('', '','','','', [])
	results = []
	if(request.session.get('states')):
		states = State.JsonToModelArray(request.session['states'])
		states.sort(key=lambda x: x.step, reverse=False)
	if(request.session.get('states_final')):
		states_final = State.JsonToModelArray(request.session['states_final'])
	if(request.session.get('state_now')):
		state_now = State.JsonToModel(request.session['state_now'])
	if(request.session.get('results')):
		results = json.loads(request.session['results'])

	if request.method == "GET":
		if states != None:
			if(len(states) > 0):
				if(state_now == None or state_now.step == ''):
					logger.error("Definindo state_now inicial : {0}".format(states[0]))
					state_now = states[0]
					request.session['state_now'] = Utils.ObjectToJson(state_now)
	elif request.method == "POST":
		if(len(states) > 0):	
			resultState = state_now.step
			for option in state_now.options:
				isChecked = request.POST.get(option['value'], False)
				if isChecked:
					resultState +=  '-' + option['value']
			if resultState != '':
				results.append(resultState)
			request.session['results'] = Utils.ObjectToJson(results)

			for index, item in enumerate(states):
				if item.step == state_now.step:
					break
			else:
				index = -1
			# testa se é o ultimo state
			if index == (len(states)-1):
				return redirect('conclusao')
			else:
				state_now = states[index + 1]
				request.session['state_now'] = Utils.ObjectToJson(state_now)

			return HttpResponseRedirect('leitura')
	concluido = False
	if(request.session.get('concluido')):
		if request.session['concluido']:
			concluido = True		
				

	return render(request, 'pesquisa/leitura.html', { 'states': states, 'states_final' : states_final, 'state_now' : state_now, 'concluido' : concluido })
def conclusao(request):
	results = []
	states_final = []
	if(request.session.get('states_final')):
		states_final = State.JsonToModelArray(request.session['states_final'])
	if(request.session.get('results')):
		results = json.loads(request.session['results'])
	resultAtual = ':'.join(results)
	resultAtual = resultAtual.replace('"', '')
	logger.error("resultAtual : {0}".format(resultAtual))  
	mensagens = []
	for state in states_final:
		logger.error("state : {0}".format(state))  
		if(state.name == resultAtual):
			mensagens.append(state.desc)
	if(len(mensagens) == 0):
		mensagens.append('Nenhuma observação')
	request.session['concluido'] = True
	return render(request, 'pesquisa/conclusao.html', { 'mensagens' : mensagens, 'results' : results })
def administrador(request):
	global logger
	dados = Manifest.objects.all()
	template = 'pesquisa/admin.html'
	if request.method == "GET":
		return render(request, template, { 'manifestos': dados })

	#region IMPORTAÇÃO DO MANIFESTO ATRAVÉS DE UM ARQUIVO CSV. 
	csv_file = None
	if(request.FILES.get('myfile')):
		csv_file = request.FILES['myfile']
    # checar se é um CSV
	if csv_file == None:
		messages.error(request, 'Não foi selecionado nenhum arquivo')
		return HttpResponseRedirect('administrador')
	if not csv_file.name.endswith('.csv'):
		messages.error(request, 'Não foi selecionado um arquivo CSV')
		return HttpResponseRedirect('administrador')
	
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
	#endregion IMPORTAÇÃO DO MANIFESTO ATRAVÉS DE UM ARQUIVO CSV.
	return HttpResponseRedirect('administrador')