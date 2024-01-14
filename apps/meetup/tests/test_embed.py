from __future__ import annotations

from unittest.mock import ANY, MagicMock, patch

import pytest
from django.conf import settings

from apps.meetup.embed import SpeakerDeckEmbed, YoutubeEmbed


@pytest.fixture
def response_mock():
    response = MagicMock()
    response.status_code = 200
    response.json.return_value = {"type": "rich"}
    return response


class TestSpeakerDeckEmbed:
    def test_request(self, response_mock):
        with patch("apps.meetup.embed.requests.get", return_value=response_mock) as get_mock:
            result = SpeakerDeckEmbed.request(url="test-url")

        assert result == {"type": "rich"}
        get_mock.assert_called_once_with(
            url="https://speakerdeck.com/oembed.json",
            params={"url": "test-url"},
            timeout=(SpeakerDeckEmbed.READ_TIMEOUT, SpeakerDeckEmbed.CONNECT_TIMEOUT),
        )


class TestYoutubeEmbed:
    def test_request(self, response_mock):
        with patch("apps.meetup.embed.requests.get", return_value=response_mock) as get_mock:
            result = YoutubeEmbed.request(url="test-url")

        assert result == {"type": "rich", "width": settings.EMBED_VIDEO_WIDTH, "height": settings.EMBED_VIDEO_HEIGHT}
        get_mock.assert_called_once_with(
            url="https://youtube.com/oembed",
            params={"url": "test-url", "format": "json"},
            timeout=(SpeakerDeckEmbed.READ_TIMEOUT, SpeakerDeckEmbed.CONNECT_TIMEOUT),
        )

    def test_request__adjust_iframe_size(self, response_mock):
        response_mock.json.return_value = {"html": '<iframe width="100" height="200" src="test"></iframe>'}

        with patch("apps.meetup.embed.requests.get", return_value=response_mock) as get_mock:
            result = YoutubeEmbed.request(url="test-url")

        assert result == {"width": settings.EMBED_VIDEO_WIDTH, "height": settings.EMBED_VIDEO_HEIGHT, "html": ANY}
        assert 'height="480"' in result["html"]
        assert 'width="854"' in result["html"]
        get_mock.assert_called_once_with(
            url="https://youtube.com/oembed",
            params={"url": "test-url", "format": "json"},
            timeout=(SpeakerDeckEmbed.READ_TIMEOUT, SpeakerDeckEmbed.CONNECT_TIMEOUT),
        )
