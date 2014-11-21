from django.contrib import admin
from django.contrib.auth.models import User

from mailator.models import *


class LayoutAdmin(admin.ModelAdmin):
  list_display = ('name', 'content')

class OptoutCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'public')

class EmailListAdmin(admin.ModelAdmin):
    list_display = ('name', 'format', 'sep', 'nb_emails')

class ConnectionAdmin(admin.ModelAdmin):
    list_display = ('name', 'host', 'port', 'username', 'password', 'use_tls', 'use_ssl')

class TypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'connection', 'layout', 'category', 'description', 'email_from')

class TemplateAdmin(admin.ModelAdmin):
    list_display = ('email_type', 'lang', 'subject')

class TaskAdmin(admin.ModelAdmin):
    list_display = ('name', 'datetime', 'liste', 'email', 'processed', 'step')

admin.site.register(Layout, LayoutAdmin)
admin.site.register(OptoutCategory, OptoutCategoryAdmin)
admin.site.register(EmailList, EmailListAdmin)
admin.site.register(Connection, ConnectionAdmin)
admin.site.register(Type, TypeAdmin)
admin.site.register(Template, TemplateAdmin)
admin.site.register(Task, TaskAdmin)


