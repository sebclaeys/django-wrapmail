# coding=utf-8
__author__ = 'sebastienclaeys'

from django.db import models
from const import *
from django.core.cache import cache
from django.core.validators import validate_email

class BlacklistManager(models.Manager):
    def add_emails(self, emails):
        bulk = []
        for email in emails:
            email = email.strip()
            try:
                validate_email( email )
                bulk.append(Blacklist(email=email))
            except:
                # Email does not match email regex. Skipping
                pass

        self.bulk_create(bulk)
        cache.delete('mailator_blacklist')
        print "%s item added to the blacklist" % len(bulk)
        return len(bulk)

    def get_set(self):
        blacklist_set = cache.get('mailator_blacklist', None)
        if blacklist_set is None:
            blacklist_set = set(map(lambda x: x.email, self.all()))
            cache.set('mailator_blacklist', blacklist_set)
        return blacklist_set


class Blacklist(models.Model):
    email = models.CharField(max_length=128, blank=True)

    objects = BlacklistManager()

    def __unicode__(self):
        return self.email

    class Meta:
        app_label = APP_NAME

