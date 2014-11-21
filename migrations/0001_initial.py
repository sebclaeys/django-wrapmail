# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Layout'
        db.create_table(u'mailator_layout', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=64, db_index=True)),
            ('content', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('mailator', ['Layout'])

        # Adding model 'OptoutCategory'
        db.create_table(u'mailator_optoutcategory', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=64, db_index=True)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('public', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal('mailator', ['OptoutCategory'])

        # Adding model 'Recipient'
        db.create_table(u'mailator_recipient', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('email', self.gf('django.db.models.fields.EmailField')(unique=True, max_length=75)),
            ('no_send', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('mailator', ['Recipient'])

        # Adding model 'OptoutRecipient'
        db.create_table(u'mailator_optoutrecipient', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('category', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['mailator.OptoutCategory'])),
            ('recipient', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['mailator.Recipient'])),
            ('optout', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('mailator', ['OptoutRecipient'])

        # Adding model 'EmailList'
        db.create_table(u'mailator_emaillist', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=64, db_index=True)),
            ('format', self.gf('django.db.models.fields.CharField')(default='email|first_name|last_name', max_length=128)),
            ('sep', self.gf('django.db.models.fields.CharField')(default='|', max_length=4)),
        ))
        db.send_create_signal('mailator', ['EmailList'])

        # Adding model 'EmailItem'
        db.create_table(u'mailator_emailitem', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('email', self.gf('django.db.models.fields.EmailField')(unique=True, max_length=75)),
            ('list', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['mailator.EmailList'])),
            ('fields', self.gf('django.db.models.fields.CharField')(max_length=128, blank=True)),
        ))
        db.send_create_signal('mailator', ['EmailItem'])

        # Adding model 'Connection'
        db.create_table(u'mailator_connection', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=64, db_index=True)),
            ('host', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('port', self.gf('django.db.models.fields.IntegerField')(default=587)),
            ('username', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('password', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('use_tls', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('use_ssl', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('mailator', ['Connection'])

        # Adding model 'Type'
        db.create_table(u'mailator_type', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=64, db_index=True)),
            ('connection', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['mailator.Connection'])),
            ('category', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['mailator.OptoutCategory'])),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('email_from', self.gf('django.db.models.fields.CharField')(default=None, max_length=64, null=True)),
            ('nb_sent', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('max_sent', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('layout', self.gf('django.db.models.fields.CharField')(default='email', max_length=64)),
            ('schedule', self.gf('django.db.models.fields.CharField')(default=u'none', max_length=30)),
            ('can_optout', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('manual_send', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('occurences', self.gf('django.db.models.fields.CharField')(default='', max_length=30, blank=True)),
        ))
        db.send_create_signal('mailator', ['Type'])

        # Adding model 'TypeRecipient'
        db.create_table(u'mailator_typerecipient', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('emailtype', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['mailator.Type'])),
            ('recipient', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['mailator.Recipient'])),
            ('nb_sent', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('optout', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('last_send', self.gf('django.db.models.fields.DateField')(default=None, null=True)),
        ))
        db.send_create_signal('mailator', ['TypeRecipient'])

        # Adding model 'Template'
        db.create_table(u'mailator_template', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('email_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['mailator.Type'])),
            ('lang', self.gf('django.db.models.fields.CharField')(max_length=4)),
            ('subject', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('html_content', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('mailator', ['Template'])

        # Adding unique constraint on 'Template', fields ['email_type', 'lang']
        db.create_unique(u'mailator_template', ['email_type_id', 'lang'])

        # Adding model 'Event'
        db.create_table(u'mailator_event', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75)),
            ('event', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('processed', self.gf('django.db.models.fields.BooleanField')(default=False, db_index=True)),
        ))
        db.send_create_signal('mailator', ['Event'])


    def backwards(self, orm):
        # Removing unique constraint on 'Template', fields ['email_type', 'lang']
        db.delete_unique(u'mailator_template', ['email_type_id', 'lang'])

        # Deleting model 'Layout'
        db.delete_table(u'mailator_layout')

        # Deleting model 'OptoutCategory'
        db.delete_table(u'mailator_optoutcategory')

        # Deleting model 'Recipient'
        db.delete_table(u'mailator_recipient')

        # Deleting model 'OptoutRecipient'
        db.delete_table(u'mailator_optoutrecipient')

        # Deleting model 'EmailList'
        db.delete_table(u'mailator_emaillist')

        # Deleting model 'EmailItem'
        db.delete_table(u'mailator_emailitem')

        # Deleting model 'Connection'
        db.delete_table(u'mailator_connection')

        # Deleting model 'Type'
        db.delete_table(u'mailator_type')

        # Deleting model 'TypeRecipient'
        db.delete_table(u'mailator_typerecipient')

        # Deleting model 'Template'
        db.delete_table(u'mailator_template')

        # Deleting model 'Event'
        db.delete_table(u'mailator_event')


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
            'description': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
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
            'OptoutCategories': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['mailator.OptoutCategory']", 'through': "orm['mailator.OptoutRecipient']", 'symmetrical': 'False'}),
            'email': ('django.db.models.fields.EmailField', [], {'unique': 'True', 'max_length': '75'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'no_send': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'mailator.template': {
            'Meta': {'unique_together': "(('email_type', 'lang'),)", 'object_name': 'Template'},
            'email_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['mailator.Type']"}),
            'html_content': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lang': ('django.db.models.fields.CharField', [], {'max_length': '4'}),
            'subject': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        },
        'mailator.type': {
            'Meta': {'object_name': 'Type'},
            'can_optout': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['mailator.OptoutCategory']"}),
            'connection': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['mailator.Connection']"}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'email_from': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '64', 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'layout': ('django.db.models.fields.CharField', [], {'default': "'email'", 'max_length': '64'}),
            'manual_send': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'max_sent': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '64', 'db_index': 'True'}),
            'nb_sent': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'occurences': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '30', 'blank': 'True'}),
            'recipients': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['mailator.Recipient']", 'through': "orm['mailator.TypeRecipient']", 'symmetrical': 'False'}),
            'schedule': ('django.db.models.fields.CharField', [], {'default': "u'none'", 'max_length': '30'})
        },
        'mailator.typerecipient': {
            'Meta': {'object_name': 'TypeRecipient'},
            'emailtype': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['mailator.Type']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_send': ('django.db.models.fields.DateField', [], {'default': 'None', 'null': 'True'}),
            'nb_sent': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'optout': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'recipient': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['mailator.Recipient']"})
        }
    }

    complete_apps = ['mailator']