# -*- coding: utf-8 -*-
import os

from unittest import TestCase
from mock import Mock

from moscowdjango.wsgi import force_domain


class ForceDomainTest(TestCase):

    def setUp(self):
        self.app = force_domain(Mock(name='app'))
        self.start_response = Mock(name='start_response')

    def test_no_domain_set(self):
        if os.environ.get('DOMAIN'):
            del os.environ['DOMAIN']
        self.app({'HTTP_HOST': 'testserver'}, self.start_response)
        self.assertEqual(self.start_response.call_count, 0)

    def test_domain_set_not_equal(self):
        os.environ['DOMAIN'] = 'other_server/mypage'
        self.app({'HTTP_HOST': 'testserver'}, self.start_response)
        self.start_response.assert_called_once_with('301 Redirect', [('Location', 'http://other_server/mypage')])

    def test_domain_set_equal(self):
        os.environ['DOMAIN'] = 'testserver'
        self.app({'HTTP_HOST': 'testserver'}, self.start_response)
        self.assertEqual(self.start_response.call_count, 0)
