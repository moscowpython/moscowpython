# -*- coding: utf-8 -*-
from unittest import TestCase
from mock import patch, MagicMock
from meetup.views import ajax_subscribe


@patch.dict('os.environ', TIMEPAD_API_KEY='xxx', TIMEPAD_ORG_ID='123', TIMEPAD_MAILLIST_ID='1')
class SubscribeTest(TestCase):

    def setUp(self):
        self.request = MagicMock(name='email subscribe')
        self.request.POST.__getitem__.return_value = 'foo@bar.buz'

    @patch('meetup.utils.requests.get')
    def test_email_ok(self, requests_mock):
        requests_mock.return_value = MagicMock(status_code=200, json={
            'itemsDuplicate': 0,
            'itemsWrongFormat': 0,
            'result': "ok",
            'itemsAdded': 1
        })
        response = ajax_subscribe(self.request)
        self.assertEquals(response.content, 'OK')

    @patch('meetup.utils.requests.get')
    def test_email_fail(self, requests_mock):
        requests_mock.return_value = MagicMock(status_code=200, json={
            'error': "wrong_code"
        })
        response = ajax_subscribe(self.request)
        self.assertEquals(response.content, 'Failed')