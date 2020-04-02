#
# Created on Tue Mar 31 2020
#
# Copyright (c) 2020 Maurício André Kunz
# mauricioandrek@hotmail.com
#
import json
from django.conf import settings
from django.db import models
from typing import List
import logging

class Option(models.Model):
    step = models.TextField()
    value = models.TextField()
    desc = models.TextField()

    def __str__(self):
        return self.value

class State(models.Model):
    step = models.TextField()
    name = models.TextField()
    desc = models.TextField()
    model = models.TextField()
    marker = models.TextField()
    options = []
    def __str__(self):
        return self.name
    def __init__(self, step: str, name: str, desc: str, model: str, marker: str, options: List[Option] ):
        self.step = step
        self.name = name
        self.desc = desc
        self.model = model
        self.marker = marker
        self.options = options

    @classmethod
    def JsonToModelArray(obj, value):
        try:
            arr = []
            for item in json.loads(value):
                d = json.loads(item)
                arr.append(State(**d))
            return arr
        except Exception as e:
            logging.exception("Erro ao transformar json para array de objetos, model: {0} json: {1}".format(model, value))
            return [] 
    @classmethod
    def JsonToModel(obj, value):
        try:
            d = json.loads(value)
            return State(**json.loads(value))
        except Exception as e:
            logging.exception("Erro ao transformar json para objeto, model: {0} json: {1}".format(model, value))
            return None
