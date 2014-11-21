Django Emailer - Manage multilingul email templates
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
                'filename': '/var/log/mailator/activity.log',
            },
            'mailator_error': {
                'level': 'ERROR',
                'class': 'logging.FileHandler',
                'filename': '/var/log/mailator/error.log',
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


### Templates

In settings.py:

    TEMPLATE_DIRS = (
        '%s/mailator/templates' % BASE
     )

### Assets

In apache conf:

    Alias /mailator/pub/ <base>/mailator/pub/

    <Directory <base>/mailator/pub>
       Options Includes FollowSymLinks MultiViews
       Order allow,deny
       Allow from all
    </Directory>



## Recuring tasks

Requires django celry

In settings.py:

    

    CELERYBEAT_SCHEDULE = {
        'email_daily_am': { 'task': 'mailator.tasks.process_scheduled_task', 'args': ('daily_am',),
            'schedule': crontab(hour=10, minute=17)
        },
        'email_daily_pm': { 'task': 'mailator.tasks.process_scheduled_task', 'args': ('daily_pm',),
            'schedule': crontab(hour=14, minute=13)
        },
        'email_weekly_mon': { 'task': 'mailator.tasks.process_scheduled_task', 'args': ('weekly_mon',),
            'schedule': crontab(hour=10, minute=17, day_of_week='mon')
        },
        'email_weekly_tue': { 'task': 'mailator.tasks.process_scheduled_task', 'args': ('weekly_tue',),
            'schedule': crontab(hour=10, minute=17, day_of_week='tue')
        },
        'email_weekly_wed': { 'task': 'mailator.tasks.process_scheduled_task', 'args': ('weekly_wed',),
            'schedule': crontab(hour=10, minute=17, day_of_week='wed')
        },
        'email_weekly_thu': { 'task': 'mailator.tasks.process_scheduled_task', 'args': ('weekly_thu',),
            'schedule': crontab(hour=10, minute=17, day_of_week='thu')
        },
        'email_weekly_fri': { 'task': 'mailator.tasks.process_scheduled_task', 'args': ('weekly_fri',),
            'schedule': crontab(hour=10, minute=17, day_of_week='fri')
        },
        'email_weekly_sat': { 'task': 'mailator.tasks.process_scheduled_task', 'args': ('weekly_sat',),
            'schedule': crontab(hour=10, minute=17, day_of_week='sat')
        },
        'email_weekly_sun': { 'task': 'mailator.tasks.process_scheduled_task', 'args': ('weekly_sun',),
            'schedule': crontab(hour=10, minute=17, day_of_week='sun')
        },
        'email_monthly_1': { 'task': 'mailator.tasks.process_scheduled_task', 'args': ('monthly_1',),
            'schedule': crontab(hour=10, minute=17, day_of_month=1)
        },
        'email_monthly_2': { 'task': 'mailator.tasks.process_scheduled_task', 'args': ('monthly_2',),
            'schedule': crontab(hour=10, minute=17, day_of_month=8)
        },
        'email_monthly_3': { 'task': 'mailator.tasks.process_scheduled_task', 'args': ('monthly_3',),
            'schedule': crontab(hour=10, minute=17, day_of_month=15)
        },
        'email_monthly_4': { 'task': 'mailator.tasks.process_scheduled_task', 'args': ('monthly_4',),
            'schedule': crontab(hour=10, minute=17, day_of_month=22)
        },
    }



