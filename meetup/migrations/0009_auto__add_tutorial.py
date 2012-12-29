# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Tutorial'
        db.create_table('meetup_tutorial', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=250)),
            ('slug', self.gf('django.db.models.fields.SlugField')(default='', max_length=50)),
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(null=True, to=orm['meetup.Speaker'], blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('content', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('meetup', ['Tutorial'])


    def backwards(self, orm):
        # Deleting model 'Tutorial'
        db.delete_table('meetup_tutorial')


    models = {
        'meetup.event': {
            'Meta': {'object_name': 'Event', 'ordering': "['-date']"},
            'date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'null': 'True', 'blank': 'True', 'max_length': '100'}),
            'manual_on_air': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True', 'default': 'None'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '1024'}),
            'number': ('django.db.models.fields.SmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'sponsors': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'to': "orm['meetup.Sponsor']", 'symmetrical': 'False'}),
            'status': ('model_utils.fields.StatusField', [], {'no_check_for_status': 'True', 'default': "'draft'", 'max_length': '100'}),
            'status_changed': ('model_utils.fields.MonitorField', [], {'monitor': "'status'", 'default': 'datetime.datetime.now'}),
            'timepad_id': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'default': '0'}),
            'venue': ('django.db.models.fields.related.ForeignKey', [], {'null': 'True', 'to': "orm['meetup.Venue']", 'blank': 'True'})
        },
        'meetup.mediacoverage': {
            'Meta': {'object_name': 'MediaCoverage'},
            'event': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'media_coverages'", 'to': "orm['meetup.Event']"}),
            'ico': ('django.db.models.fields.CharField', [], {'null': 'True', 'blank': 'True', 'max_length': '250'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        },
        'meetup.photo': {
            'Meta': {'object_name': 'Photo'},
            'caption': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'event': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'photos'", 'null': 'True', 'to': "orm['meetup.Event']", 'blank': 'True'}),
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
            'photo': ('django.db.models.fields.files.ImageField', [], {'null': 'True', 'blank': 'True', 'max_length': '100'}),
            'slug': ('django.db.models.fields.SlugField', [], {'default': "''", 'max_length': '50'})
        },
        'meetup.sponsor': {
            'Meta': {'object_name': 'Sponsor'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'logo': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'url': ('django.db.models.fields.URLField', [], {'blank': 'True', 'max_length': '200'})
        },
        'meetup.talk': {
            'Meta': {'object_name': 'Talk', 'ordering': "('-event__number', 'position')"},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'event': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'talks'", 'to': "orm['meetup.Event']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '1024'}),
            'position': ('django.db.models.fields.SmallIntegerField', [], {'default': '0'}),
            'presentation': ('django.db.models.fields.URLField', [], {'blank': 'True', 'max_length': '200'}),
            'presentation_data': ('picklefield.fields.PickledObjectField', [], {'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'}),
            'speaker': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'talks'", 'to': "orm['meetup.Speaker']"}),
            'status': ('model_utils.fields.StatusField', [], {'no_check_for_status': 'True', 'default': "'draft'", 'max_length': '100'}),
            'status_changed': ('model_utils.fields.MonitorField', [], {'monitor': "'status'", 'default': 'datetime.datetime.now'}),
            'video': ('django.db.models.fields.URLField', [], {'blank': 'True', 'max_length': '200'}),
            'video_data': ('picklefield.fields.PickledObjectField', [], {'blank': 'True'})
        },
        'meetup.tutorial': {
            'Meta': {'object_name': 'Tutorial'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'null': 'True', 'to': "orm['meetup.Speaker']", 'blank': 'True'}),
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
            'latitude': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '9', 'decimal_places': '6', 'blank': 'True'}),
            'longitude': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '9', 'decimal_places': '6', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['meetup']