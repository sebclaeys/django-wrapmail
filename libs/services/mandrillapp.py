# coding=utf-8
__author__ = 'Sébastien Claeys'

import mandrill

def send_message(subject, html_content, text_content, to, from_email, context):
    from_name = ""
    to_name = ""
    if 'name' in context:
        to_name = context['name']
    elif 'first_name' in context:
        to_name = context['first_name']
        if 'last_name' in context:
            to_name += " %s" %  context['last_name']

    if '<' in from_email:
        from_name, from_email = map(lambda x: x.strip().strip('>'), from_email.split('<'))

    mandrill_client = mandrill.Mandrill('kriKzIy-hK9bpzxC1TiodQ')
    message = {'from_email': from_email,
               'from_name': from_name,
               'headers': {'Reply-To': from_email},
               'html': html_content,
               'subject': subject,
               'text': text_content,
               'to': [{'email': to,
                       'name': to_name,
                       'type': 'to'}],
               'track_clicks': True,
               'track_opens': True
    }

    from datetime import datetime
    result = mandrill_client.messages.send(message=message, async=True, ip_pool='Main Pool', send_at=datetime.now().strftime("%Y%m%d %H:%M:%S"))
    return result