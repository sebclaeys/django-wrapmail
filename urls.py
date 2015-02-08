__author__ = 'sebastienclaeys'

from django.conf.urls import url, patterns

urlpatterns = patterns('mailator.views',
    (r'^$', 'dashboard'),
    # (r'^connections$', 'connection'),
    # (r'^emails$', 'emails'),
    # (r'^lists$', 'lists'),
    # (r'^connections$', 'subscriptions'),

    (r'^tasks/$', 'tasks'),
    (r'^send_email/$', 'send_email'),
    (r'^edit_email/(\d+)$', 'edit_email'),
    (r'^edit_template/(\d+)$', 'edit_template'),
    (r'^save_template/(\d+)/(\w+)$', 'save_template'),
    (r'^preview_layout/(\d+)$', 'preview_layout'),
    (r'^preview_template/(\d+)/(\d+)$', 'preview_template'),
    (r'^edit_list/(\d+)$', 'edit_list'),
    (r'^compute_stats/(\d+)$', 'compute_stats'),
    (r'^upload_list/(\d+)$', 'upload_list'),
    (r'^edit_task/(\d+)$', 'edit_task'),
    (r'^task_logs/(\d+)$', 'task_logs'),
    (r'^task_status/(\d+)$', 'task_status'),
    (r'^play_task/(\d+)$', 'play_task'),
    (r'^unsubscribe/(\d+)/([0-9a-zA-Z_=-]+)$', 'unsubscribe'),
    (r'^spamreport/([0-9a-zA-Z_=-]+)$', 'spamreport'),
    (r'^mandrill_events/$', 'mandrill_events'),
    (r'^blacklist/$', 'blacklist'),
    (r'^upload_blacklist/$', 'upload_blacklist'),
)
