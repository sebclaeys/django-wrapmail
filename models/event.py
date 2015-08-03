# coding=utf-8
__author__ = 'sclaeys'

from django.db import models
from const import *
import logging

class Event(models.Model):
    email = models.EmailField()
    event = models.CharField(max_length=30)
    processed = models.BooleanField(default=False, db_index=True)


    class Meta:
        app_label = APP_NAME


class EmailEventManager(models.Manager):
    def add_event(self, event, email_name=None, recipient=None):
        return self.create(email_name=email_name, event=event, recipient=recipient)

    def add_sendgrid_event(self, events):

        for event in events:
            email_name = None
            if 'email_name' in event:
                email_name = event['email_name']
            self.add_event(event['event'], recipient=event['email'], email_name=email_name)

    def add_mandrill_event(self, events):
        pass

    def aggregate_date_range(self, start_date=None, end_date=None):
        qs = self.all()

        if start_date:
            qs = qs.filter(created__gt=start_date)

        if end_date:
            qs = qs.filter(created__lt=end_date)

        res = {}

        for item in qs:
            if not item.email_name in res:
                res[item.email_name] = {}

            if not item.event in res[item.email_name]:
                res[item.email_name][item.event] = 0

            res[item.email_name][item.event] += 1

        for key, item in res.iteritems():
            if 'delivered' in item:
                delivered = item['delivered']
                if 'open' in item:
                    item['open_rate'] = (item['open'] * 100) / delivered

                if 'click' in item:
                    item['click_rate'] = (item['click'] * 100) / delivered

        return res

class EmailEvent(models.Model):
    email_name = models.CharField(max_length=255, default=None, null=True)
    recipient = models.CharField(max_length=255, default=None, null=True)
    event = models.CharField(max_length=255, default=None, null=True)
    created = models.DateTimeField(auto_now_add=True)

    objects = EmailEventManager()

    class Meta:
        app_label = APP_NAME
