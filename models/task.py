# coding=utf-8
__author__ = 'sebastienclaeys'

from django.db import models
from const import *
from django.conf import settings as conf
from mailator.libs import sender

from mailator.models.list import EmailList
from mailator.models.connection import Connection
from mailator.models.emailer import Type

class TaskManager(models.Manager):
    def to_process(self, schedule):
        return self.filter(schedule=schedule, completed=False, errors=False, processing=False)

import traceback

class Task(models.Model):
    name = models.CharField(max_length=64, default='Manual send')
    lang = models.CharField(max_length=4, choices=conf.LANGUAGES, default='en')
    datetime = models.DateTimeField(auto_now_add=True)
    connection_override = models.ForeignKey(Connection, default=None, null=True, blank=True)
    from_override = models.CharField(max_length=64, default=None, blank=True, null=True)
    liste = models.ForeignKey(EmailList)
    email = models.ForeignKey(Type)
    exclude_members = models.BooleanField(default=False)
    logs = models.TextField(blank=True)
    concurrency = models.PositiveSmallIntegerField(default=1)

    step = models.PositiveIntegerField(default=100)
    processed = models.PositiveIntegerField(default=0)
    growth = models.FloatField(default=0)

    # Old way
    # steps = models.PositiveIntegerField(default=1)
    # progress = models.IntegerField(default=0)

    processing = models.BooleanField(default=False)
    schedule = models.CharField(max_length=30, db_index=True, choices=EMAIL_SCHEDULES, default=u'none')
    errors = models.BooleanField(default=False)
    completed = models.BooleanField(default=False)

    # Override default manager
    objects = TaskManager()


    def status(self):
        if self.errors:
            return "Error"
        if self.processing:
            return "Running"
        if self.completed:
            return "Completed"
        if self.schedule == u'none':
            return "Paused"
        return "Scheduled"

    def nb_processed(self):
        # Old way
        # step_items = self.liste.nb_emails / self.steps
        # return step_items * self.progress
        return self.processed

    def percent(self):
        return (self.processed * 100) / self.liste.nb_emails

    def log(self, str):
        print str
        self.logs = self.logs + str + '\n'
        #self.save()

    # Return tuple:
    # (bounce_rate, spam_rate, open_rate, click_rate)
    def get_stats(self):
        liste = self.liste
        nb_processed = self.nb_processed()
        spam_rate = (liste.spam * 100.0) / nb_processed
        click_rate = (liste.click * 100.0) / nb_processed
        open_rate = (liste.open * 100.0) / nb_processed
        bounce_rate = (liste.bounce * 100.0) / nb_processed

        return (bounce_rate, spam_rate, open_rate, click_rate)


    def process(self, processes=None):
        # Process one step of this task


        processes = processes if processes else self.concurrency

        if self.completed or self.percent() >= 100 or self.errors:
            self.log("Task can not be processed")
            return

        # 0 Set the task as processing
        self.processing = True

        # Flush preview logs
        self.logs = "Starting new processing"
        self.save()

        # 1 get the portion of the list taking steps and progress
        recipients = self.liste.build_recipient_list(self.processed, self.step)
        total_to_process = len(recipients)

        # 1.2 - exclude blacklists
        skipped = 0
        if self.exclude_members:
            from django.contrib.auth.models import User
            blacklist = set(map(lambda x: x.email, User.objects.all()))
            filtered_list = []
            for r in recipients:
                if r.email in blacklist:
                    skipped += 1
                    print "Email skipped - Already member, #%d" % skipped
                else:
                    filtered_list.append(r)

            recipients = filtered_list


        # 2 Try to send emails to that list and passing a callback to fill the log string. Also set the connection override if exists
        try:
            total_members, count, blacklisted, member_skiped, errors = sender.multiprocess_send_to_recipients(recipients, self.email.name, context={}, lang=self.lang, connection_override=self.connection_override, log_call=self.log, processes=processes, from_override=self.from_override if self.from_override and len(self.from_override) else None)
            print "Task completed. %d/%d sent, %d blacklisted, %d member_skipped, %d errors" % (count, total_members, blacklisted, skipped, errors)

            # 5 update the progress
            self.processed += total_to_process
            self.step += int(self.step * self.growth / 100.0)
        except Exception, e:
            # 3 If an arror occurs, mark the task as 'has errors'
            self.log("An unexpected error occured: " + str(e))
            self.log(traceback.format_exc())
            self.errors = True
            self.save()


        # 6 if we have reach the number of steps, mark the task as done
        if self.processed >= self.liste.nb_emails:
            self.completed = True

        # 7 set processing as false
        self.processing = False
        self.save()


    def __unicode__(self):
        return self.name

    class Meta:
        app_label = APP_NAME
