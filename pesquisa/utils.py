#
# Created on Tue Mar 31 2020
#
# Copyright (c) 2020 Maurício André Kunz
# mauricioandrek@hotmail.com
#
import json
from collections import namedtuple, Iterable
from django.forms.models import model_to_dict
from .other_models import State
import logging
logger = logging.getLogger(__name__)
class Utils(object):
    @staticmethod
    def NOME_APLICACAO():
        return "Aplicação de AR para uso em aulas práticas de medicina"
    @staticmethod
    def DESCRICAO_APLICACAO():
        return "O objetivo desse aplicativo é permitir que alunos utilizem realidade aumentada (AR) na sala de aula de uma forma ativa. Nesse caso, os próprios alunos podem produzir e organizar os conteúdos visualizados pelo aplicativo."
    
    @staticmethod
    def ObjectToJson(obj):
        global logger
        json_ = ''
        if isinstance(obj, Iterable):
            if len(obj) == 1:
                json_ = json.dumps(obj, default=lambda o: o.__dict__)
            else:
                json_ = json.dumps(["{0}".format(json.dumps(ob, default=lambda o: o.__dict__)) for ob in obj])
        else:
            json_ = json.dumps(obj, default=lambda o: o.__dict__)
        return json_
            