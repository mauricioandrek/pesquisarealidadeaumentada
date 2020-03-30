from django.conf import settings
from django.db import models
from django.utils import timezone


class Manifest(models.Model):
    _step = models.TextField()
    _type = models.TextField()
    _value = models.TextField()
    _desc = models.TextField()
    _imported_date = models.DateTimeField(blank=True, null=True)

    def publish(self):
        self._imported_date = timezone.now()
        self.save()

    def __str__(self):
        return self._value

    def getType(self):
        return self._type
    def getValue(self):
        return self._value
    def getDesc(self):
        return self._desc
