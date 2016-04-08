Django Wrapmail - Manage Multilingul Transactional email templates
It helps you manage emails internally and leave you completly intependent from you SMTP provider.

You can connect Django Wrapmail to Sendgrid, Mandril, Mailjet and other 3rd party email providers, or just connect it to you own SMTP server.
==========

## Requirements

## Settings

In settings.py:

    # Allow mailator to override email connections
    # Should be False for all dev config to prevent emails to be sent
    MAILATOR_OVERRIDE = True

    # Send email tasks to django celery
    # Should be on only for Production settings
    MAILATOR_ASYNC = True

## Logging

    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'handlers': {
            'mailator_activity': {
                'level': 'INFO',
                'class': 'logging.FileHandler',
                'filename': '/var/log/django-wrapmail/activity.log',
            },
            'mailator_error': {
                'level': 'ERROR',
                'class': 'logging.FileHandler',
                'filename': '/var/log/django-wrapmail/error.log',
            },
        },
        'loggers': {
            'mailator.activity': {
                'handlers': ['mailator_activity'],
                'level': 'INFO',
                'propagate': False,
            },
            'mailator.error': {
                'handlers': ['mailator_error'],
                'level': 'ERROR',
                'propagate': False,
            },
        }
    }





