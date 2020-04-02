from django.conf import settings
from django.db import models
from django.utils import timezone
#
# Created on Tue Mar 31 2020
#
# Copyright (c) 2020 Maurício André Kunz
# mauricioandrek@hotmail.com
#

class Manifest(models.Model):
    step = models.TextField()
    typee = models.TextField()
    value = models.TextField()
    desc = models.TextField()
    imported_date = models.DateTimeField(blank=True, null=True)

    def publish(self):
        self._imported_date = timezone.now()
        self.save()

    def __str__(self):
        return self.value

    def getType(self):
        return self.typee
    def getValue(self):
        return self.value
    def getDesc(self):
        return self.desc


    