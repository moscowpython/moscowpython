# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Vacancy'
        db.create_table('vacancies_vacancy', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('model_utils.fields.AutoCreatedField')(default=datetime.datetime.now)),
            ('modified', self.gf('model_utils.fields.AutoLastModifiedField')(default=datetime.datetime.now)),
            ('status', self.gf('model_utils.fields.StatusField')(default='active', max_length=100, no_check_for_status=True)),
            ('status_changed', self.gf('model_utils.fields.MonitorField')(default=datetime.datetime.now, monitor='status')),
            ('company', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('contacts', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('type', self.gf('django.db.models.fields.CharField')(default='fulltime', max_length=50)),
            ('is_participant', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_priority', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('vacancies', ['Vacancy'])


    def backwards(self, orm):
        # Deleting model 'Vacancy'
        db.delete_table('vacancies_vacancy')


    models = {
        'vacancies.vacancy': {
            'Meta': {'object_name': 'Vacancy'},
            'company': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'contacts': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'created': ('model_utils.fields.AutoCreatedField', [], {'default': 'datetime.datetime.now'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_participant': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_priority': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'modified': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'status': ('model_utils.fields.StatusField', [], {'default': "'active'", 'max_length': '100', 'no_check_for_status': 'True'}),
            'status_changed': ('model_utils.fields.MonitorField', [], {'default': 'datetime.datetime.now', 'monitor': "'status'"}),
            'type': ('django.db.models.fields.CharField', [], {'default': "'fulltime'", 'max_length': '50'})
        }
    }

    complete_apps = ['vacancies']