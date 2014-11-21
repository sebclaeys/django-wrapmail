# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'TypeRecipient'
        db.delete_table(u'mailator_typerecipient')

        # Deleting field 'Type.schedule'
        db.delete_column(u'mailator_type', 'schedule')

        # Deleting field 'Type.nb_sent'
        db.delete_column(u'mailator_type', 'nb_sent')

        # Deleting field 'Type.manual_send'
        db.delete_column(u'mailator_type', 'manual_send')

        # Deleting field 'Type.max_sent'
        db.delete_column(u'mailator_type', 'max_sent')

        # Deleting field 'Type.can_optout'
        db.delete_column(u'mailator_type', 'can_optout')

        # Deleting field 'Type.occurences'
        db.delete_column(u'mailator_type', 'occurences')


        # Renaming column for 'Type.layout' to match new field type.
        db.rename_column(u'mailator_type', 'layout', 'layout_id')
        # Changing field 'Type.layout'
        db.alter_column(u'mailator_type', 'layout_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['mailator.Layout']))
        # Adding index on 'Type', fields ['layout']
        db.create_index(u'mailator_type', ['layout_id'])


    def backwards(self, orm):
        # Removing index on 'Type', fields ['layout']
        db.delete_index(u'mailator_type', ['layout_id'])

        # Adding model 'TypeRecipient'
        db.create_table(u'mailator_typerecipient', (
            ('last_send', self.gf('django.db.models.fields.DateField')(default=None, null=True)),
            ('optout', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('emailtype', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['mailator.Type'])),
            ('nb_sent', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('recipient', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['mailator.Recipient'])),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('mailator', ['TypeRecipient'])

        # Adding field 'Type.schedule'
        db.add_column(u'mailator_type', 'schedule',
                      self.gf('django.db.models.fields.CharField')(default=u'none', max_length=30),
                      keep_default=False)

        # Adding field 'Type.nb_sent'
        db.add_column(u'mailator_type', 'nb_sent',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)

        # Adding field 'Type.manual_send'
        db.add_column(u'mailator_type', 'manual_send',
                      self.gf('django.db.models.fields.BooleanField')(default=True),
                      keep_default=False)

        # Adding field 'Type.max_sent'
        db.add_column(u'mailator_type', 'max_sent',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)

        # Adding field 'Type.can_optout'
        db.add_column(u'mailator_type', 'can_optout',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'Type.occurences'
        db.add_column(u'mailator_type', 'occurences',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=30, blank=True),
                      keep_default=False)


        # Renaming column for 'Type.layout' to match new field type.
        db.rename_column(u'mailator_type', 'layout_id', 'layout')
        # Changing field 'Type.layout'
        db.alter_column(u'mailator_type', 'layout', self.gf('django.db.models.fields.CharField')(max_length=64))

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
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['mailator.OptoutCategory']"}),
            'connection': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['mailator.Connection']"}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'email_from': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '64', 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'layout': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['mailator.Layout']"}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '64', 'db_index': 'True'})
        }
    }

    complete_apps = ['mailator']