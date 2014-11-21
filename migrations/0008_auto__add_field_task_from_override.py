# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Task.from_override'
        db.add_column(u'mailator_task', 'from_override',
                      self.gf('django.db.models.fields.CharField')(default=None, max_length=64, null=True, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Task.from_override'
        db.delete_column(u'mailator_task', 'from_override')


    models = {
        'mailator.connection': {
            'Meta': {'object_name': 'Connection'},
            'host': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '64', 'db_index': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'port': ('django.db.models.fields.IntegerField', [], {'default': '587'}),
            'use_ssl': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'use_tls': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        },
        'mailator.emailitem': {
            'Meta': {'object_name': 'EmailItem'},
            'email': ('django.db.models.fields.EmailField', [], {'unique': 'True', 'max_length': '75'}),
            'fields': ('django.db.models.fields.CharField', [], {'max_length': '128', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'list': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['mailator.EmailList']"})
        },
        'mailator.emaillist': {
            'Meta': {'object_name': 'EmailList'},
            'format': ('django.db.models.fields.CharField', [], {'default': "'email|first_name|last_name'", 'max_length': '128'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64', 'db_index': 'True'}),
            'nb_emails': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'sep': ('django.db.models.fields.CharField', [], {'default': "'|'", 'max_length': '4'})
        },
        'mailator.event': {
            'Meta': {'object_name': 'Event'},
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'event': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'processed': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'})
        },
        'mailator.layout': {
            'Meta': {'object_name': 'Layout'},
            'content': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '64', 'db_index': 'True'})
        },
        'mailator.optoutcategory': {
            'Meta': {'object_name': 'OptoutCategory'},
            'can_optout': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'group': ('django.db.models.fields.CharField', [], {'default': "'trampolinn'", 'max_length': '32', 'db_index': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'link_override': ('django.db.models.fields.TextField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '64', 'db_index': 'True'}),
            'public': ('django.db.models.fields.BooleanField', [], {'default': 'True'})
        },
        'mailator.optoutrecipient': {
            'Meta': {'object_name': 'OptoutRecipient'},
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['mailator.OptoutCategory']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'optout': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'recipient': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['mailator.Recipient']"})
        },
        'mailator.recipient': {
            'Meta': {'object_name': 'Recipient'},
            'email': ('django.db.models.fields.EmailField', [], {'unique': 'True', 'max_length': '75'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'no_send': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'optoutcategories': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['mailator.OptoutCategory']", 'through': "orm['mailator.OptoutRecipient']", 'symmetrical': 'False'})
        },
        'mailator.task': {
            'Meta': {'object_name': 'Task'},
            'completed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'connection_override': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': "orm['mailator.Connection']", 'null': 'True', 'blank': 'True'}),
            'datetime': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['mailator.Type']"}),
            'errors': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'from_override': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '64', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lang': ('django.db.models.fields.CharField', [], {'default': "'en'", 'max_length': '4'}),
            'liste': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['mailator.EmailList']"}),
            'logs': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "'Manual send'", 'max_length': '64'}),
            'processing': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'progress': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'schedule': ('django.db.models.fields.CharField', [], {'default': "u'none'", 'max_length': '30', 'db_index': 'True'}),
            'steps': ('django.db.models.fields.PositiveIntegerField', [], {'default': '1'})
        },
        'mailator.template': {
            'Meta': {'unique_together': "(('email_type', 'lang'),)", 'object_name': 'Template'},
            'email_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['mailator.Type']"}),
            'html_content': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lang': ('django.db.models.fields.CharField', [], {'max_length': '4'}),
            'subject': ('django.db.models.fields.CharField', [], {'max_length': '128', 'blank': 'True'})
        },
        'mailator.type': {
            'Meta': {'object_name': 'Type'},
            'category': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': "orm['mailator.OptoutCategory']", 'null': 'True'}),
            'connection': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['mailator.Connection']"}),
            'description': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '128'}),
            'email_from': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '64'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'layout': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['mailator.Layout']"}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '64', 'db_index': 'True'})
        }
    }

    complete_apps = ['mailator']