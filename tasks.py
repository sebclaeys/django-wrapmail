__author__ = 'sebastienclaeys'

from celery import task
from mailator.libs import sender
import mailator.models as model
import mailator.conf as conf

@task
def send_to_recipients(recipients, email_name, context=None, lang=None, connection_override=None, from_override=None):
    sender.send_to_recipients(recipients, email_name, context=context, lang=lang, connection_override=connection_override, from_override=from_override)


# EMAIL_SCHEDULES = (
#         (u'none', u'None'),
#         (u'daily_am', u'Daily - Morning'),
#         (u'daily_pm', u'Daily - Afternoon'),
#         (u'weekly_mon', u'Weekly - Monday'),
#         (u'weekly_tue', u'Weekly - Tuesday'),
#         (u'weekly_wed', u'Weekly - Wednesday'),
#         (u'weekly_thu', u'Weekly - Thursday'),
#         (u'weekly_fri', u'Weekly - Friday'),
#         (u'weekly_sat', u'Weekly - Saterday'),
#         (u'weekly_sun', u'Weekly - Sunday'),
#         (u'monthly_1', u'Monthly @ 1st week'),
#         (u'monthly_2', u'Monthly @ 2st week'),
#         (u'monthly_3', u'Monthly @ 3st week'),
#         (u'monthly_4', u'Monthly @ 4st week'),
#     )

@task
def process_scheduled_task(schedule):
    for t in model.Task.objects.to_process(schedule):
        print "Processing task <%s>" % t.name
        t.process()

@task
def launch_task(tid):
    t = model.Task.objects.get(pk=tid)
    print "Launching task %s" % t.name
    t.process()


@task
def compute_stats(lid):
    liste = model.EmailList.objects.get(pk=int(lid))
    liste.aggregate_events()


@task
def process_mandrill_events(events):
    for event in events:
        try:
            print event
            print "Processing Mandrill event %s" % event['event']
            if event['event'] in conf.MANDRILL_EVENT_MAP.keys():
                model.Recipient.objects.process_event(event['msg']['email'], event['event'])
            else:
                print "Error: Mapping for event %s not found" % event['event']
        except Exception, e:
            print "Error: Unable to process event: %s" % str(e)


