# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Talk'
        db.create_table('meetup_talk', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('status', self.gf('model_utils.fields.StatusField')(default='draft', max_length=100, no_check_for_status=True)),
            ('status_changed', self.gf('model_utils.fields.MonitorField')(default=datetime.datetime.now, monitor='status')),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=1024)),
            ('speaker', self.gf('django.db.models.fields.related.ForeignKey')(related_name='talks', to=orm['meetup.Speaker'])),
            ('event', self.gf('django.db.models.fields.related.ForeignKey')(related_name='talks', to=orm['meetup.Event'])),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('presentation', self.gf('django.db.models.fields.URLField')(max_length=200, blank=True)),
            ('presentation_data', self.gf('picklefield.fields.PickledObjectField')(blank=True)),
            ('video', self.gf('django.db.models.fields.URLField')(max_length=200, blank=True)),
            ('video_data', self.gf('picklefield.fields.PickledObjectField')(blank=True)),
        ))
        db.send_create_signal('meetup', ['Talk'])

        # Adding model 'Event'
        db.create_table('meetup_event', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('status', self.gf('model_utils.fields.StatusField')(default='draft', max_length=100, no_check_for_status=True)),
            ('status_changed', self.gf('model_utils.fields.MonitorField')(default=datetime.datetime.now, monitor='status')),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=1024)),
            ('number', self.gf('django.db.models.fields.SmallIntegerField')(null=True, blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True)),
            ('date', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('venue', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['meetup.Venue'], null=True, blank=True)),
        ))
        db.send_create_signal('meetup', ['Event'])

        # Adding M2M table for field sponsors on 'Event'
        db.create_table('meetup_event_sponsors', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('event', models.ForeignKey(orm['meetup.event'], null=False)),
            ('sponsor', models.ForeignKey(orm['meetup.sponsor'], null=False))
        ))
        db.create_unique('meetup_event_sponsors', ['event_id', 'sponsor_id'])

        # Adding model 'Venue'
        db.create_table('meetup_venue', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('address', self.gf('django.db.models.fields.TextField')()),
            ('latitude', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=9, decimal_places=6, blank=True)),
            ('longitude', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=9, decimal_places=6, blank=True)),
        ))
        db.send_create_signal('meetup', ['Venue'])

        # Adding model 'Speaker'
        db.create_table('meetup_speaker', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('photo', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True)),
            ('company_name', self.gf('django.db.models.fields.CharField')(max_length=1024, blank=True)),
        ))
        db.send_create_signal('meetup', ['Speaker'])

        # Adding model 'Photo'
        db.create_table('meetup_photo', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('event', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='photos', null=True, to=orm['meetup.Event'])),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=100, blank=True)),
            ('caption', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal('meetup', ['Photo'])

        # Adding model 'Sponsor'
        db.create_table('meetup_sponsor', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=250)),
            ('logo', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200, blank=True)),
        ))
        db.send_create_signal('meetup', ['Sponsor'])


    def backwards(self, orm):
        # Deleting model 'Talk'
        db.delete_table('meetup_talk')

        # Deleting model 'Event'
        db.delete_table('meetup_event')

        # Removing M2M table for field sponsors on 'Event'
        db.delete_table('meetup_event_sponsors')

        # Deleting model 'Venue'
        db.delete_table('meetup_venue')

        # Deleting model 'Speaker'
        db.delete_table('meetup_speaker')

        # Deleting model 'Photo'
        db.delete_table('meetup_photo')

        # Deleting model 'Sponsor'
        db.delete_table('meetup_sponsor')


    models = {
        'meetup.event': {
            'Meta': {'ordering': "['-date']", 'object_name': 'Event'},
            'date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '1024'}),
            'number': ('django.db.models.fields.SmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'sponsors': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['meetup.Sponsor']", 'symmetrical': 'False', 'blank': 'True'}),
            'status': ('model_utils.fields.StatusField', [], {'default': "'draft'", 'max_length': '100', 'no_check_for_status': 'True'}),
            'status_changed': ('model_utils.fields.MonitorField', [], {'default': 'datetime.datetime.now', 'monitor': "'status'"}),
            'venue': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['meetup.Venue']", 'null': 'True', 'blank': 'True'})
        },
        'meetup.photo': {
            'Meta': {'object_name': 'Photo'},
            'caption': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'event': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'photos'", 'null': 'True', 'to': "orm['meetup.Event']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        },
        'meetup.speaker': {
            'Meta': {'object_name': 'Speaker'},
            'company_name': ('django.db.models.fields.CharField', [], {'max_length': '1024', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'photo': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'})
        },
        'meetup.sponsor': {
            'Meta': {'object_name': 'Sponsor'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'logo': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'})
        },
        'meetup.talk': {
            'Meta': {'object_name': 'Talk'},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'event': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'talks'", 'to': "orm['meetup.Event']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '1024'}),
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