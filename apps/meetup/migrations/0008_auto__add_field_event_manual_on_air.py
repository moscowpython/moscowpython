# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Event.manual_on_air'
        db.add_column('meetup_event', 'manual_on_air',
                      self.gf('django.db.models.fields.NullBooleanField')(default=None, null=True, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Event.manual_on_air'
        db.delete_column('meetup_event', 'manual_on_air')


    models = {
        'meetup.event': {
            'Meta': {'ordering': "['-date']", 'object_name': 'Event'},
            'date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'manual_on_air': ('django.db.models.fields.NullBooleanField', [], {'default': 'False', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '1024'}),
            'number': ('django.db.models.fields.SmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'sponsors': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['meetup.Sponsor']", 'symmetrical': 'False', 'blank': 'True'}),
            'status': ('model_utils.fields.StatusField', [], {'default': "'draft'", 'max_length': '100', 'no_check_for_status': 'True'}),
            'status_changed': ('model_utils.fields.MonitorField', [], {'default': 'datetime.datetime.now', 'monitor': "'status'"}),
            'timepad_id': ('django.db.models.fields.IntegerField', [], {'default': '0', 'blank': 'True'}),
            'venue': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['meetup.Venue']", 'null': 'True', 'blank': 'True'})
        },
        'meetup.mediacoverage': {
            'Meta': {'object_name': 'MediaCoverage'},
            'event': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'media_coverages'", 'to': "orm['meetup.Event']"}),
            'ico': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        },
        'meetup.photo': {
            'Meta': {'object_name': 'Photo'},
            'caption': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'event': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'photos'", 'null': 'True', 'to': "orm['meetup.Event']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'})
        },
        'meetup.speaker': {
            'Meta': {'object_name': 'Speaker'},
            'company_name': ('django.db.models.fields.CharField', [], {'max_length': '1024', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'photo': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'default': "''", 'max_length': '50'})
        },
        'meetup.sponsor': {
            'Meta': {'object_name': 'Sponsor'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'logo': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'})
        },
        'meetup.talk': {
            'Meta': {'ordering': "('-event__number', 'position')", 'object_name': 'Talk'},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'event': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'talks'", 'to': "orm['meetup.Event']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '1024'}),
            'position': ('django.db.models.fields.SmallIntegerField', [], {'default': '0'}),
            'presentation': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'presentation_data': ('picklefield.fields.PickledObjectField', [], {'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'}),
            'speaker': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'talks'", 'to': "orm['meetup.Speaker']"}),
            'status': ('model_utils.fields.StatusField', [], {'default': "'draft'", 'max_length': '100', 'no_check_for_status': 'True'}),
            'status_changed': ('model_utils.fields.MonitorField', [], {'default': 'datetime.datetime.now', 'monitor': "'status'"}),
            'video': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'video_data': ('picklefield.fields.PickledObjectField', [], {'blank': 'True'})
        },
        'meetup.venue': {
            'Meta': {'object_name': 'Venue'},
            'address': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'latitude': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '9', 'decimal_places': '6', 'blank': 'True'}),
            'longitude': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '9', 'decimal_places': '6', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['meetup']