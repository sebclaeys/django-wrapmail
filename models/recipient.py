# coding=utf-8
__author__ = 'sclaeys'

from django.db import models
from const import *

class OptoutCategoryManager(models.Manager):
    def byGroup(self, group):
        return self.filter(can_optout=True, group=group)


class OptoutCategory(models.Model):
    name = models.CharField(max_length=64, unique=True, db_index=True)
    description = models.TextField()
    public = models.BooleanField(default=True)  # Public optout category (can be triggered without being logged in)
    can_optout = models.BooleanField(default=True)
    group = models.CharField(max_length=32, default='trampolinn', db_index=True)

    # By default a link is generated to optout of this category. But a custom link can be provided
    link_override = models.TextField(default=None, blank=True, null=True)

    objects = OptoutCategoryManager()

    def __unicode__(self):
        return self.name

    class Meta:
        app_label = APP_NAME


class RecipientManager(models.Manager):
    def process_event(self, email, event):
        try:
            recipient, created = self.get_or_create(email=email)

            if event == 'spam':
                recipient.spam += 1
            elif event == 'bounce':
                recipient.bounce += 1
            elif event == 'open':
                recipient.open += 1
            elif event == 'click':
                recipient.click += 1
            else:
                print "Unknown event type %s" % event
                return
            recipient.save()
        except:
            print "Recipient <%s> does not exists" % email


class Recipient(models.Model):
    email = models.EmailField(unique=True, db_index=True)
    no_send = models.BooleanField(default=False)  # Email flagged as no send
    optoutcategories = models.ManyToManyField(OptoutCategory, through='OptoutRecipient')

    spam = models.IntegerField(default=0)
    bounce = models.IntegerField(default=0)
    open = models.IntegerField(default=0)
    click = models.IntegerField(default=0)

    objects = RecipientManager()

    def __unicode__(self):
        return self.email

    class Meta:
        app_label = APP_NAME


class OptoutRecipientManager(models.Manager):
    def is_optout(self, category, email):
        a = self.filter(category=category, recipient__email=email)
        if a:
            return a[0].optout
        return False

class OptoutRecipient(models.Model):
    category = models.ForeignKey(OptoutCategory)
    recipient = models.ForeignKey(Recipient)
    optout = models.BooleanField(default=False)

    objects = OptoutRecipientManager()

    class Meta:
        app_label = APP_NAME

