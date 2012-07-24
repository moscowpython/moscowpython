# -*- coding: utf-8 -*-
from unittest.case import TestCase

from mock import Mock, patch, MagicMock
from meetup.views import ajax_subscribe


class SubscribeTest(TestCase):

    def setUp(self):
        self.request = MagicMock()
        self.request.POST.__getitem__.return_value = 'foo@bar.buz'

    @patch('meetup.utils.requests.post')
    def test_email_ok(self, response_mock):
        response_mock.return_value = MagicMock(status_code=200, text=u'Поздравляем, Вы подписались')
        response = ajax_subscribe(self.request)
        self.assertEquals(response.content, 'OK')

    @patch('meetup.utils.requests.post')
    def test_email_fail(self, response_mock):
        response_mock.return_value = MagicMock(status_code=200, text=u'Все плохо')
        response = ajax_subscribe(self.request)
        self.assertEquals(response.content, 'Failed')