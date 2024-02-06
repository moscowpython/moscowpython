from __future__ import annotations

import datetime
from unittest.mock import patch, Mock
from django.test import TestCase, override_settings
from embedly import Embedly
from requests import Response

from apps.meetup.models import Event, Speaker, Talk


class FakeOembed:
    _data = {"key": "value"}


class MockResponse(Response):
    def __init__(self, url, headers={'Content-Type': 'text/html; charset=UTF-8'}, status_code=200):
        self.url = url
        self.headers = headers
        self.status_code = status_code


class TalkTestCase(TestCase):
    def setUp(self):
        self.event = Event.objects.create(date=datetime.datetime(2015, 5, 16, 2, 0, 0), name="test")
        self.speaker = Speaker.objects.create(name="test", slug="test")

    @override_settings(EMBEDLY_KEY="internal")
    @patch('requests.get', Mock(side_effect=[
        MockResponse("http://example.com/video/"),
        MockResponse("http://example.com/presentation/"),
    ]))
    def test_set_embedly_data(self):
        talk = Talk.objects.create(event=self.event, speaker=self.speaker, name="test")
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
