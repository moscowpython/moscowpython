# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Vacancy.salary'
        db.add_column('vacancies_vacancy', 'salary',
                      self.gf('django.db.models.fields.CharField')(blank=True, default='', max_length=100),
                      keep_default=False)

        # Adding field 'Vacancy.url'
        db.add_column('vacancies_vacancy', 'url',
                      self.gf('django.db.models.fields.URLField')(default='', unique=True, max_length=200),
                      keep_default=False)

        # Adding field 'Vacancy.published_at'
        db.add_column('vacancies_vacancy', 'published_at',
                      self.gf('django.db.models.fields.DateTimeField')(null=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Vacancy.salary'
        db.delete_column('vacancies_vacancy', 'salary')

        # Deleting field 'Vacancy.url'
        db.delete_column('vacancies_vacancy', 'url')

        # Deleting field 'Vacancy.published_at'
        db.delete_column('vacancies_vacancy', 'published_at')


    models = {
        'vacancies.vacancy': {
            'Meta': {'object_name': 'Vacancy', 'ordering': "['-is_priority', '-published_at']"},
            'company': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'contacts': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'created': ('model_utils.fields.AutoCreatedField', [], {'default': 'datetime.datetime.now'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_participant': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_priority': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'modified': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'published_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'salary': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '100'}),
            'status': ('model_utils.fields.StatusField', [], {'default': "'active'", 'no_check_for_status': 'True', 'max_length': '100'}),
            'status_changed': ('model_utils.fields.MonitorField', [], {'monitor': "'status'", 'default': 'datetime.datetime.now'}),
            'type': ('django.db.models.fields.CharField', [], {'default': "'fulltime'", 'max_length': '50'}),
            'url': ('django.db.models.fields.URLField', [], {'unique': 'True', 'max_length': '200'})
        }
    }

    complete_apps = ['vacancies']