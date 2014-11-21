# coding=utf-8
__author__ = 'sclaeys'

from django.db import models
from const import *

class Connection(models.Model):
    name = models.CharField(max_length=64, unique=True, db_index=True)
    host = models.CharField(max_length=128)
    port = models.IntegerField(default=587)
    username = models.CharField(max_length=128)
    password = models.CharField(max_length=128)
    use_tls = models.BooleanField(default=True)
    use_ssl = models.BooleanField(default=False)

    def __unicode__(self):
        return self.name

    def to_kwargs(self):
        return {'host': str(self.host),
                'port': int(self.port),
                'username': str(self.username),
                'password': str(self.password),
                'use_tls': self.use_tls,
                'use_ssl': self.use_ssl}

    class Meta:
        app_label = APP_NAME
