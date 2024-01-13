from __future__ import annotations

from logging import getLogger
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup
from django.conf import settings
from embedly.client import Embedly

logger = getLogger(__name__)


class BaseEmbed:
    URL = None
    READ_TIMEOUT = 3
    CONNECT_TIMEOUT = 3
    PARAMS = {}

    @classmethod
    def request(cls, url: str) -> dict:
        params = {"url": url}
        params.update(cls.PARAMS)
        resp = requests.get(url=cls.URL, params=params, timeout=(cls.READ_TIMEOUT, cls.CONNECT_TIMEOUT))

        if resp.status_code != 200:
            raise Exception(f"Error: {resp.status_code}")

        return resp.json()


class SpeakerDeckEmbed(BaseEmbed):
    URL = "https://speakerdeck.com/oembed.json"


class YoutubeEmbed(BaseEmbed):
    URL = "https://youtube.com/oembed"
    PARAMS = {"format": "json"}

    @classmethod
    def request(cls, url: str) -> dict:
        data = super().request(url)
        w, h = settings.EMBED_VIDEO_WIDTH, settings.EMBED_VIDEO_HEIGHT
        data['width'] = w
        data['height'] = h

        html = data.get('html') or ''

        soup = BeautifulSoup(html, features="html.parser")
        iframe = soup.find('iframe')

        if iframe is None:
            logger.warning("Iframe not found in youtube emded code, video size won't be adjusted")
            return html

        iframe['width'] = w
        iframe['height'] = h

        data['html'] = str(iframe)
        return data


class EmbedlyEmbed:
    @classmethod
    def request(cls, url: str) -> dict:
        embedly_key = getattr(settings, 'EMBEDLY_KEY')
        if embedly_key is None or embedly_key == '':
            raise Exception("no embedly key")

        client = Embedly(embedly_key)
        response = client.oembed(url)
        return response._data


adapters = {"speakerdeck.com": SpeakerDeckEmbed, "youtube.com": YoutubeEmbed, "youtu.be": YoutubeEmbed}


def get_domain(url: str) -> str:
    parts = urlparse(url).netloc
    return '.'.join(parts.split('.')[-2:])


def get_embed_data(url: str | None) -> dict | None:
    if url is None or url == '':
        return None

    domain = get_domain(url)
    adapter = adapters.get(domain, EmbedlyEmbed)

    try:
        return adapter.request(url)
    except Exception:
        return None
