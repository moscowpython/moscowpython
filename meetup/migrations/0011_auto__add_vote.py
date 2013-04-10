# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Vote'
        db.create_table('meetup_vote', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('model_utils.fields.AutoCreatedField')(default=datetime.datetime.now)),
            ('modified', self.gf('model_utils.fields.AutoLastModifiedField')(default=datetime.datetime.now)),
            ('talk', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['meetup.Talk'], related_name='votes')),
            ('event', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['meetup.Event'], related_name='votes')),
            ('ua', self.gf('django.db.models.fields.TextField')()),
            ('ip', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('meetup', ['Vote'])

        # Adding field 'Event.votable'
        db.add_column('meetup_event', 'votable',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting model 'Vote'
        db.delete_table('meetup_vote')

        # Deleting field 'Event.votable'
        db.delete_column('meetup_event', 'votable')


    models = {
        'meetup.event': {
            'Meta': {'object_name': 'Event', 'ordering': "['-date']"},
            'date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'manual_on_air': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'default': 'None', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '1024'}),
            'number': ('django.db.models.fields.SmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'sponsors': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['meetup.Sponsor']", 'blank': 'True', 'symmetrical': 'False'}),
            'status': ('model_utils.fields.StatusField', [], {'max_length': '100', 'default': "'planning'", 'no_check_for_status': 'True'}),
            'status_changed': ('model_utils.fields.MonitorField', [], {'default': 'datetime.datetime.now', 'monitor': "'status'"}),
            'timepad_id': ('django.db.models.fields.IntegerField', [], {'default': '0', 'blank': 'True'}),
            'venue': ('django.db.models.fields.related.ForeignKey', [], {'null': 'True', 'to': "orm['meetup.Venue']", 'blank': 'True'}),
            'votable': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'meetup.mediacoverage': {
            'Meta': {'object_name': 'MediaCoverage'},
            'event': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['meetup.Event']", 'related_name': "'media_coverages'"}),
            'ico': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        },
        'meetup.photo': {
            'Meta': {'object_name': 'Photo'},
            'caption': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'event': ('django.db.models.fields.related.ForeignKey', [], {'null': 'True', 'to': "orm['meetup.Event']", 'blank': 'True', 'related_name': "'photos'"}),
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
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'default': "''"})
        },
        'meetup.sponsor': {
            'Meta': {'object_name': 'Sponsor'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'logo': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'})
        },
        'meetup.talk': {
            'Meta': {'object_name': 'Talk', 'ordering': "('-event__number', 'position')"},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'event': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['meetup.Event']", 'related_name': "'talks'"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '1024'}),
            'position': ('django.db.models.fields.SmallIntegerField', [], {'default': '0'}),
            'presentation': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'presentation_data': ('picklefield.fields.PickledObjectField', [], {'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'}),
            'speaker': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['meetup.Speaker']", 'related_name': "'talks'"}),
            'status': ('model_utils.fields.StatusField', [], {'max_length': '100', 'default': "'active'", 'no_check_for_status': 'True'}),
            'status_changed': ('model_utils.fields.MonitorField', [], {'default': 'datetime.datetime.now', 'monitor': "'status'"}),
            'video': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'video_data': ('picklefield.fields.PickledObjectField', [], {'blank': 'True'})
        },
        'meetup.tutorial': {
            'Meta': {'object_name': 'Tutorial'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'null': 'True', 'to': "orm['meetup.Speaker']", 'blank': 'True'}),
            'content': ('django.db.models.fields.TextField', [], {}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'default': "''"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '250'})
        },
        'meetup.venue': {
            'Meta': {'object_name': 'Venue'},
            'address': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'latitude': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'blank': 'True', 'decimal_places': '6', 'max_digits': '9'}),
            'longitude': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'blank': 'True', 'decimal_places': '6', 'max_digits': '9'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'meetup.vote': {
            'Meta': {'object_name': 'Vote'},
            'created': ('model_utils.fields.AutoCreatedField', [], {'default': 'datetime.datetime.now'}),
            'event': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['meetup.Event']", 'related_name': "'votes'"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip': ('django.db.models.fields.TextField', [], {}),
            'modified': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'}),
            'talk': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['meetup.Talk']", 'related_name': "'votes'"}),
            'ua': ('django.db.models.fields.TextField', [], {})
        }
    }

    complete_apps = ['meetup']