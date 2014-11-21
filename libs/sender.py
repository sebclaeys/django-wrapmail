from django.core.mail import get_connection, EmailMultiAlternatives
import logging
from django.utils import translation
from django.template import Template, Context
import mailator.libs.helper as helper

import mailator.conf as conf

log_info = logging.getLogger("mailator.info")
log_error = logging.getLogger("mailator.error")

from django.contrib.auth.models import User
MEMBERS = set(map(lambda x: x.email, User.objects.all()))

from multiprocessing import Pool

def log_info(msg, callback=None):
    logger = logging.getLogger("mailator.info")
    logger.info(msg)
    if callback:
        callback(msg)

def log_error(msg, callback=None):
    logger = logging.getLogger("mailator.error")
    logger.error(msg)
    if callback:
        callback(msg)


EMAIL_LIMIT_PER_CO=100

def print_logger(str):
    print str

def set_lang(lang):
    translation.activate(lang)

import os

def send_message(subject, html_content, text_content, to, from_email=None, connection=None, attachment=None):
    msg = EmailMultiAlternatives(subject, text_content, from_email, to, connection=connection)
    msg.attach_alternative(html_content, "text/html")
    if attachment and os.path.exists(attachment.path):
        msg.attach_file(attachment.path)
    msg.send()
    import django.core.mail.message

def send_to_list(liste, email_name, context={}, lang=None):
    return send_to_recipients(liste.build_recipient_list(), email_name, context, lang)


def multiprocess_send_to_recipients(recipients, email_name, context={}, lang=None, connection_override=None, log_call=print_logger, from_override=None, processes=1):
    if processes == 1:
        # Use the regular function if we have only one process
        return send_to_recipients(recipients, email_name, context=context, lang=lang, connection_override=connection_override, log_call=log_call, from_override=from_override)

    # Create a wrapper that contains all sub parameters and takes only the chunk of recipient
    def wrapper(recipients_chunk):
        return send_to_recipients(recipients_chunk , email_name, context=context, lang=lang, connection_override=connection_override, log_call=log_call, from_override=from_override)


    from multiprocessing.pool import ThreadPool
    pool = ThreadPool(processes=processes)

    # Prepare sublist of recipients to be distributed accross the threads
    # Numpy help us to split our list of recipients into sublist of roughly the same size
    import numpy
    sub_recipient_lists = map(lambda x: x.tolist(), numpy.array_split(numpy.array(recipients), processes))

    # Aggregate the result of each thread
    total_members, count, blacklisted, member_skiped, errors = (0,0,0,0,0)
    for t_total_members, t_count, t_blacklisted, t_member_skiped, t_errors in pool.map(wrapper, sub_recipient_lists):
        total_members += t_total_members
        count += t_count
        blacklisted += t_blacklisted
        member_skiped += t_member_skiped
        errors += t_errors

    return (total_members, count, blacklisted, member_skiped, errors)


def send_to_recipients(recipients, email_name, context={}, lang=None, connection_override=None, log_call=print_logger, from_override=None):
    import mailator.models as model
    connection = None
    count = 0
    total = 0
    limit = EMAIL_LIMIT_PER_CO
    total_members = len(recipients)
    blacklist = model.Blacklist.objects.get_set()
    blacklisted = 0
    member_skiped = 0
    errors = 0
    opted_out = 0

    try:
        email_obj = model.Type.objects.get(name=email_name)
    except Exception, e:
        log_error("Failed to send emails:" + str(e), callback=log_call)
        return

    layout = email_obj.layout

    for recipient in recipients:
        try:
            if recipient.email in blacklist:
                blacklisted += 1
                log_info("Skiping email <%s>. Blacklisted #%d" % (recipient.email, blacklisted), callback=log_call)
                continue

            if email_obj.exclude_members and recipient.email in MEMBERS:
                member_skiped += 1
                log_info("Skiping email <%s>. Already member #%d" % (recipient.email, member_skiped), callback=log_call)
                continue

            if model.OptoutRecipient.objects.is_optout(email_obj.category, recipient.email):
                opted_out += 1
                log_info("Skiping email <%s>. Opted out of this category #%d" % (recipient.email, opted_out), callback=log_call)
                continue

            log_info("sending email to <%s>. %d/%d" % (recipient.email, total, total_members), callback=log_call)
            if total % limit == 0 or connection is None:
                if connection:
                    connection.close()

                if conf.MAILATOR_OVERRIDE:
                    con_kwargs = email_obj.connection.to_kwargs() if not connection_override else connection_override.to_kwargs()
                    connection = get_connection(**con_kwargs)
                else:
                    connection = get_connection()
                connection.open()
            total += 1

            context.update(recipient.__dict__)
            context.update({'user': recipient})


            if not lang:
                try:
                    if recipient.lang:
                        lang = recipient.lang
                    else:
                        lang = 'en'
                except:
                    lang = 'en'

            # Lang context override
            if 'lang' in context:
                lang = context['lang']

            set_lang(lang)

            template = email_obj.template_set.filter(lang=lang)

            if not template:
                # Template not found, fall back to english
                template = email_obj.template_set.filter(lang='en')
                if not template:
                    # English template not found, fall back to first template
                    # Let the exception raise if no templates
                    template = email_obj.template_set.all()


            tmpl = template[0]
            ctx = Context(context)
            subject = Template(tmpl.subject).render(ctx)
            from_email = from_override if (from_override and len(from_override)) else email_obj.email_from
            from_email = from_email % context

            html_content = Template(layout.content % {'content': tmpl.html_content, 'optout_link': email_obj.get_optout_link(recipient.email)}).render(ctx)
            text_content = helper.html_to_text(html_content)

            send_message(subject, html_content, text_content, [recipient.email], from_email=from_email, connection=connection, attachment=tmpl.attachment)

            count += 1

        except Exception, e:
            import traceback
            log_error(traceback.format_exc())
            log_error("Failed to send email:" + str(e), callback=log_call)
            errors += 1
            connection = None

    log_info("Email sent to %d out of %d members. %d blacklisted, %d member skipped, %d errors" % (count, total_members, blacklisted, member_skiped, errors), callback=log_call)
    if connection:
        connection.close()


    return (total_members, count, blacklisted, member_skiped, errors)

