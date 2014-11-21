# coding=utf-8
__author__ = 'sclaeys'

from django.db import models
from const import *

class Event(models.Model):
    email = models.EmailField()
    event = models.CharField(max_length=30)
    processed = models.BooleanField(default=False, db_index=True)

    class Meta:
        app_label = APP_NAME
