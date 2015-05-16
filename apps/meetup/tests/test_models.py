# coding: utf-8
import datetime
from django.test import TestCase, override_settings
from unittest.mock import patch
from embedly import Embedly
from apps.meetup.models import Talk, Event, Speaker


class FakeOembed():
    _data = {"key": "value"}


class TalkTestCase(TestCase):

    def setUp(self):
        self.event = Event.objects.create(
            date=datetime.datetime(2015, 5, 16, 2, 0, 0),
            name="test",

        )
        self.speaker = Speaker.objects.create(
            name="test",
            slug="test",
        )

    @override_settings(EMBEDLY_KEY="internal")
    def test_set_embedly_data(self):
        talk = Talk.objects.create(
            event=self.event,
            speaker=self.speaker,
            name="test"
        )
        with patch.object(Embedly, 'oembed', return_value=FakeOembed()) as oembed:
            talk.presentation = "http://example.com/presentation/"
            talk.video = "http://example.com/video/"
            talk.save()

        self.assertEqual(oembed.call_count, 2)
        oembed.assert_any_call("http://example.com/presentation/")
        oembed.assert_any_call("http://example.com/video/")

        self.assertEqual(talk.presentation, "http://example.com/presentation/")
        self.assertEqual(talk.video, "http://example.com/video/")
        self.assertEqual(talk.presentation_data, {"key": "value"})
        self.assertEqual(talk.video_data, {"key": "value"})

        with patch.object(Embedly, 'oembed', return_value=FakeOembed()) as oembed:
            talk.presentation = ""
            talk.video = ""
            talk.save()

        self.assertEqual(oembed.call_count, 0)

        self.assertEqual(talk.presentation, "")
        self.assertEqual(talk.video, "")
        self.assertEqual(talk.presentation_data, "")
        self.assertEqual(talk.video_data, "")
