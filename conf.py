from django.conf import settings

# Allow mailator to override email connections
# Should be False for all dev config to prevent emails to be sent
MAILATOR_OVERRIDE = getattr(settings, 'MAILATOR_OVERRIDE', True)

# Send email tasks to django celery
# Should be on only for Production settings
MAILATOR_ASYNC = getattr(settings, 'MAILATOR_ASYNC', True)

# send, deferral, hard_bounce, soft_bounce, open, click, spam, unsub, reject
MANDRILL_EVENT_MAP = {'hard_bounce': 'bounce',
                      'soft_bounce': 'bounce',
                      'click': 'click',
                      'spam': 'spam',
                      'unsub': 'unsub',
                      'open': 'open'
}
