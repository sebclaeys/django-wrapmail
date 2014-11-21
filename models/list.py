# coding=utf-8
__author__ = 'sclaeys'

from django.db import models
from const import *
from mailator.libs.helper import DummyRecipient
from mailator.models.recipient import Recipient

class EmailList(models.Model):
    name = models.CharField(db_index=True, max_length=64)
    format = models.CharField(max_length=128, default='email|first_name|last_name')
    sep = models.CharField(default='|', max_length=4)
    nb_emails = models.IntegerField(default=0)

    spam = models.IntegerField(default=0)
    bounce = models.IntegerField(default=0)
    open = models.IntegerField(default=0)
    click = models.IntegerField(default=0)

    def aggregate_events(self):
        # Heavy processing. To do once in a while
        sum_spam = 0
        sum_bounce = 0
        sum_open = 0
        sum_click = 0

        for item in self.emailitem_set.all():
            try:
                recipient = Recipient.objects.get(email=item.email)
                sum_spam += recipient.spam
                sum_bounce += recipient.bounce
                sum_open += recipient.open
                sum_click += recipient.click
            except:
                # Email item in the list has not been sent yet
                pass

        self.spam = sum_spam
        self.click = sum_click
        self.bounce = sum_bounce
        self.open + sum_open
        self.save()


    # def getNbEmails(self):
    #     return len(self.emailitem_set.all())

    # nb_emails = property(getNbEmails)

    def get_fields(self):
        if not '_field_list' in self.__dict__:
            self._field_list = self.format.split(self.sep)
        return self._field_list

    def overview(self):
        return self.emailitem_set.all()[:50]

    def build_recipient_list(self, start, step):
        qs = self.emailitem_set.all()[start:step+start]
        res = []
        for item in qs:
            res.append(DummyRecipient(item.email, item.get_field_map()))
        return res


    def _processBulk(self, bulk):
        try:
            EmailItem.objects.bulk_create(bulk)
        except Exception, e:
            print "Error while adding the block of email, %s" % str(e)
            print "Processing one by one"
            for i in bulk:
                try:
                    i.save()
                except:
                    print "Failed item: %s" % str(i.email)

    def processItems(self, lines):
        fields = self.get_fields()
        processed = 0

        bulk_add = []
        bulk_limit = 10000
        total = len(lines)

        for line in lines:
            line = line.decode('utf-8', 'ignore')
            items = line.strip().split(self.sep)
            if len(items) != len(fields):
                # print u"Bad formating <%s>" % unicode(line)
                continue
            bulk_add.append(EmailItem(email=items[0], list=self, fields=line.strip()))

            if len(bulk_add) >= bulk_limit:
                self._processBulk(bulk_add)
                processed += len(bulk_add)
                bulk_add = []


        if len(bulk_add):
            self._processBulk(bulk_add)
            processed += len(bulk_add)

        self.nb_emails = self.nb_emails + processed
        self.save()
        print "%d / %d item added" % (processed, len(lines))

    def __unicode__(self):
        return self.name

    class Meta:
        app_label = APP_NAME


class EmailItem(models.Model):
    email = models.EmailField()
    list = models.ForeignKey(EmailList)
    fields = models.CharField(blank=True, max_length=128)

    def get_fields(self):
        if not '_field_list' in self.__dict__:
            self._field_list = self.fields.split(self.list.sep)
        return self._field_list

    def get_field_map(self):
        if not '_field_map' in self.__dict__:
            self._field_map = {}
            keylist = self.list.get_fields()
            vallist = self.fields.split(self.list.sep)
            for key, val in zip(keylist, vallist):
                self._field_map[key] = val
        return self._field_map

    def get_field(self, field):
        map = self.get_field_map()
        try:
            return map[field]
        except:
            return None


    class Meta:
        app_label = APP_NAME
