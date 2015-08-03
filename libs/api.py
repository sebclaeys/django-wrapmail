__author__ = 'sebastienclaeys'

import mailator.models as model
import mailator.tasks as task_queue
from mailator.libs.helper import DummyRecipient
import mailator.libs.helper as helper

import mailator.conf as conf

# Return all available optout category
def get_optout_categories(group):
    return model.OptoutCategory.objects.byGroup(group)


# Return a dictionary with the state of each optout category for a givn email
def get_optout_state(email, group):
    categories = model.OptoutCategory.objects.byGroup(group)
    return {cat: model.OptoutRecipient.objects.is_optout(cat, email) for cat in categories}


# Opt in or out the given email for the given category
def optinout(email, cid, is_optout=True):
    category = model.OptoutCategory.objects.get(pk=cid)
    recipient, created = model.Recipient.objects.get_or_create(email=email)
    optout_cat, created = model.OptoutRecipient.objects.get_or_create(category=category, recipient=recipient)
    optout_cat.optout = is_optout
    optout_cat.save()


# Shortcuts
def optin(email, cid):
    optinout(email, cid, False)

def optout(email, cid):
    optinout(email, cid, True)


# Send the email to the given recipients.
def send_emails(recipients, email_name, context, lang=None, from_override=None, async=True):
    # if the recipient list is not a list of Users or DummyRecipients, create the DummyRecipient list
    if len(recipients) and type(recipients[0]) in  [str, unicode]:
        recipients = map(DummyRecipient, recipients)

    if conf.MAILATOR_ASYNC and async:
        task_queue.send_to_recipients.delay(recipients, email_name, context=context, lang=lang, from_override=from_override)
    else:
        task_queue.send_to_recipients(recipients, email_name, context=context, lang=lang, from_override=from_override)


# Takes an emailname and context and return a rendered version of the html and text of the email
def render_email(email_name, context=None, lang=None, tid=None):
    from django.template import Template, Context
    email = model.Type.objects.get(name=email_name)
    layout = email.layout
    ctx = Context(context if context else {})

    if tid:
        template = model.Template.objects.get(pk=int(tid))
    else:
        # If we don't find a template for that given language, get the first template created (default template)
        template = email.template_set.filter(lang=lang)
        if not template:
            template = email.template_set.all()
        template = template[0]

    html_content = Template(layout.content % {'content': template.html_content.replace('{%', '[').replace('%}', ']') if template else '', 'optout_link': '[optout_link]'}).render(ctx)
    text_content = helper.html_to_text(html_content).replace('\n', '<br>')

    return html_content, text_content


def save_sendgrid_events(events):
    model.EmailEvent.objects.add_sendgrid_event(events)

# Save an event
def save_events(events):
    objs = []
    for event in events:
        print "Saving event: %s -- %s" % (event['email'], event['event'])
        objs.append(model.Event(email=event['email'], event=event['event']))

    print "Flushing events to DB"
    model.Event.objects.bulk_create(objs)


