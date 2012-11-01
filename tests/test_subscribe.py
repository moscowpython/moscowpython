# -*- coding: utf-8 -*-
import os

from unittest import TestCase
from mock import patch, MagicMock

from django.core.urlresolvers import reverse
from django.test import RequestFactory

from meetup.views import ajax_subscribe


def FakeResponse(status_code, result, duplicate=0, wrong=0, added=1):
    return MagicMock(status_code=status_code, json={
        'itemsDuplicate': duplicate,
        'itemsWrongFormat': wrong,
        'result': result,
        'itemsAdded': added
    })

@patch.dict('os.environ', TIMEPAD_API_KEY='xxx', TIMEPAD_ORG_ID='123', TIMEPAD_MAILLIST_ID='1')
class SubscribeTest(TestCase):

    def setUp(self):
        self.request = MagicMock(name='email subscribe')
        self.request.POST.__getitem__.return_value = 'foo@bar.buz'
        self.request.POST.__contains__.return_value = True

    @patch('meetup.utils.requests.get')
    def test_email_ok(self, requests_mock):
        requests_mock.return_value = FakeResponse(200, "ok")
        response = ajax_subscribe(self.request)
        self.assertEquals(response.content, 'OK')

    @patch('meetup.utils.requests.get')
    def test_email_fail(self, requests_mock):
        requests_mock.return_value = MagicMock(status_code=200, json={
            'error': "wrong_code"
        })
        response = ajax_subscribe(self.request)
        self.assertEquals(response.content, 'Failed')


    def test_validate_email(self):
        from meetup.utils import validate_email
        valid_email = "This-is_valid.email@valid.domain-name.tld"
        invalid_emails = ["email with spaces@valid.domain-name.tld",
                          "email@wrong-domain", "AbraCadabra"]

        self.assertTrue(validate_email(valid_email))
        for invalid in invalid_emails:
            self.assertFalse(validate_email(invalid), "Email '{0}' shouldn't be valid".format(invalid))

    @patch('meetup.utils.requests.get')
    def test_subscribe_mail__envfail(self, requests_mock):
        from meetup.utils import subscribe_mail

        requests_mock.return_value = FakeResponse(500, "fail")

        email = "email@domain.tld"

        os.environ = {}

        self.assertFalse(subscribe_mail(email))
        self.assertFalse(requests_mock.called)

    @patch('meetup.utils.requests.get')
    def test_ajax_subscribe(self, requests_mock):

        requests_mock.return_value = FakeResponse(200, "ok")

        invalid_email = "invalid_email"
        valid_email = "email@domain.tdl"

        request = RequestFactory()

        no_email_request = request.post(reverse("subscribe"))
        no_email_response = ajax_subscribe(no_email_request)
        self.assertEqual(no_email_response.status_code, 200)
        self.assertEquals(no_email_response.content, "Failed")
        self.assertFalse(requests_mock.called)

        invalid_email_request = request.post(reverse("subscribe"),
            {"email": invalid_email})
        invalid_email_response = ajax_subscribe(invalid_email_request)
        self.assertEqual(invalid_email_response.status_code, 200)
        self.assertEquals(invalid_email_response.content, "Failed")
        self.assertFalse(requests_mock.called)

        valid_email_request = request.post(reverse("subscribe"),
            {"email": valid_email})
        valid_email_response = ajax_subscribe(valid_email_request)
        self.assertEqual(valid_email_response.status_code, 200)
        self.assertEquals(valid_email_response.content, "OK")
        self.assertTrue(requests_mock.called)
