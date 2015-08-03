# coding=utf-8

__author__ = 'sebastienclaeys'

from django.db import models
from const import *

from django.utils.translation import pgettext
from django.core.urlresolvers import reverse
import base64
from django.conf import settings as conf

from mailator.models.connection import Connection
from mailator.models.recipient import OptoutCategory

class Layout(models.Model):
    name = models.CharField(max_length=64, unique=True, db_index=True)
    content = models.TextField()

    def __unicode__(self):
        return self.name

    class Meta:
        app_label = APP_NAME


class Type(models.Model):
    name = models.CharField(max_length=64, unique=True, db_index=True)
    connection = models.ForeignKey(Connection)
    layout = models.ForeignKey(Layout)
    category = models.ForeignKey(OptoutCategory, null=True, default=None)
    description = models.CharField(max_length=128, default="")
    email_from = models.CharField(max_length=64, default="")
    reply_to = models.CharField(max_length=64, default="", blank=True)
    exclude_members = models.BooleanField(default=False)
    use_bcc = models.BooleanField(default=False)

    sent = models.IntegerField(default=0)
    open = models.IntegerField(default=0)
    click = models.IntegerField(default=0)
    bounce = models.IntegerField(default=0)
    spam = models.IntegerField(default=0)
    unsub = models.IntegerField(default=0)

    def langs(self):
        return [x.lang for x in self.template_set.all()]

    def get_optout_link(self, email):
        # If the email can not be opted out, just return nothing
        if not self.category or not self.category.can_optout:
            return ""

        # Prepare the optout link
        base = pgettext('Unsubscribe text', 'To unsubscribe from this email')
        click = pgettext('Click here link', 'click here')

        # Genere the link or use the privided override
        if self.category.link_override and len(self.category.link_override):
            link = self.category.link_override
        else:
            link = reverse('mailator.views.unsubscribe', args=(self.category.id, base64.b64encode(email)))

        return "%s <a href='%s/%s'>%s</a>" % (base, conf.SITE_BASE_URL, link, click)

    # recipients = models.ManyToManyField(Recipient, through='TypeRecipient')

    # def get_occurences(self):
    #     return map(lambda x: int(x), self.occurences.split(','))

    def __unicode__(self):
        return self.name

    class Meta:
        app_label = APP_NAME



class Template(models.Model):
    email_type = models.ForeignKey(Type)
    lang = models.CharField(max_length=4)
    subject = models.CharField(max_length=1024, blank=True)
    html_content = models.TextField(blank=True)
    attachment = models.FileField(upload_to="pub/doc", null=True, blank=True, default=None)

    # Ugly fix. no time to make a onetomany relationship. Todo: do it eventually
    attachment_2 = models.FileField(upload_to="pub/doc", null=True, blank=True, default=None)

    def __unicode__(self):
        return "%s - %s" % (self.email_type.name, self.lang)

    def text_content(self):
        # TOdo: use beautyul_soup here to generate text content from html content
        return ""

    class Meta:
        unique_together = ('email_type', 'lang')
        app_label = APP_NAME


