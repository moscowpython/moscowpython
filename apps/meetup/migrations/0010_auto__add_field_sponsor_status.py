# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Sponsor.status'
        db.add_column('meetup_sponsor', 'status',
                      self.gf('django.db.models.fields.CharField')(default='organizer', max_length=10),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Sponsor.status'
        db.delete_column('meetup_sponsor', 'status')


    models = {
        'meetup.event': {
            'Meta': {'ordering': "['-date']", 'object_name': 'Event'},
            'date': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'null': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'blank': 'True', 'null': 'True', 'max_length': '100'}),
            'manual_on_air': ('django.db.models.fields.NullBooleanField', [], {'blank': 'True', 'default': 'None', 'null': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '1024'}),
            'number': ('django.db.models.fields.SmallIntegerField', [], {'blank': 'True', 'null': 'True'}),
            'sponsors': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'blank': 'True', 'to': "orm['meetup.Sponsor']"}),
            'status': ('model_utils.fields.StatusField', [], {'no_check_for_status': 'True', 'default': "'planning'", 'max_length': '100'}),
            'status_changed': ('model_utils.fields.MonitorField', [], {'monitor': "'status'", 'default': 'datetime.datetime.now'}),
            'timepad_id': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'default': '0'}),
            'venue': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'to': "orm['meetup.Venue']", 'null': 'True'})
        },
        'meetup.mediacoverage': {
            'Meta': {'object_name': 'MediaCoverage'},
            'event': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'media_coverages'", 'to': "orm['meetup.Event']"}),
            'ico': ('django.db.models.fields.CharField', [], {'blank': 'True', 'null': 'True', 'max_length': '250'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        },
        'meetup.photo': {
            'Meta': {'object_name': 'Photo'},
            'caption': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'event': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'photos'", 'blank': 'True', 'to': "orm['meetup.Event']", 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'blank': 'True', 'max_length': '100'}),
            'url': ('django.db.models.fields.URLField', [], {'blank': 'True', 'max_length': '200'})
        },
        'meetup.speaker': {
            'Meta': {'object_name': 'Speaker'},
            'company_name': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '1024'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'photo': ('django.db.models.fields.files.ImageField', [], {'blank': 'True', 'null': 'True', 'max_length': '100'}),
            'slug': ('django.db.models.fields.SlugField', [], {'default': "''", 'max_length': '50'})
        },
        'meetup.sponsor': {
            'Meta': {'object_name': 'Sponsor'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'logo': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'url': ('django.db.models.fields.URLField', [], {'blank': 'True', 'max_length': '200'})
        },
        'meetup.talk': {
            'Meta': {'ordering': "('-event__number', 'position')", 'object_name': 'Talk'},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'event': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'talks'", 'to': "orm['meetup.Event']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '1024'}),
            'position': ('django.db.models.fields.SmallIntegerField', [], {'default': '0'}),
            'presentation': ('django.db.models.fields.URLField', [], {'blank': 'True', 'max_length': '200'}),
            'presentation_data': ('picklefield.fields.PickledObjectField', [], {'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'}),
            'speaker': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'talks'", 'to': "orm['meetup.Speaker']"}),
            'status': ('model_utils.fields.StatusField', [], {'no_check_for_status': 'True', 'default': "'active'", 'max_length': '100'}),
            'status_changed': ('model_utils.fields.MonitorField', [], {'monitor': "'status'", 'default': 'datetime.datetime.now'}),
            'video': ('django.db.models.fields.URLField', [], {'blank': 'True', 'max_length': '200'}),
            'video_data': ('picklefield.fields.PickledObjectField', [], {'blank': 'True'})
        },
        'meetup.tutorial': {
            'Meta': {'object_name': 'Tutorial'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'to': "orm['meetup.Speaker']", 'null': 'True'}),
            'content': ('django.db.models.fields.TextField', [], {}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'default': "''", 'max_length': '50'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '250'})
        },
        'meetup.venue': {
            'Meta': {'object_name': 'Venue'},
            'address': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'latitude': ('django.db.models.fields.DecimalField', [], {'max_digits': '9', 'blank': 'True', 'decimal_places': '6', 'null': 'True'}),
            'longitude': ('django.db.models.fields.DecimalField', [], {'max_digits': '9', 'blank': 'True', 'decimal_places': '6', 'null': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['meetup']