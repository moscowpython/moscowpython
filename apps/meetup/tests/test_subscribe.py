# coding: utf-8
import re
from unittest.mock import patch

from django.core.urlresolvers import reverse
from django.test import TestCase, RequestFactory
import responses

from apps.meetup.views import ajax_subscribe


@patch.dict('os.environ', TIMEPAD_API_KEY='xxx', TIMEPAD_ORG_ID='123', TIMEPAD_MAILLIST_ID='1')
class AjaxSubscribeTest(TestCase):

    def setUp(self):
        self.request = RequestFactory()

    @responses.activate
    def test_no_email(self):
        no_email_request = self.request.post(reverse("subscribe"))
        no_email_response = ajax_subscribe(no_email_request)
        self.assertEqual(no_email_response.status_code, 200)
        self.assertContains(no_email_response, "Failed")

    @responses.activate
    def test_invalid_email(self):
        invalid_email = "invalid_email"
        invalid_email_request = self.request.post(reverse("subscribe"), {"email": invalid_email})
        invalid_email_response = ajax_subscribe(invalid_email_request)
        self.assertEqual(invalid_email_response.status_code, 200)
        self.assertContains(invalid_email_response, "Failed")
        assert len(responses.calls) == 0

    @responses.activate
    def test_valid_email(self):
        responses.add(responses.GET, re.compile(r'https://timepad.ru/api/.+'),
                      body='{"result": "ok"}', status=200,
                      content_type='application/json')
        valid_email = "email@domain.tdl"
        valid_email_request = self.request.post(reverse("subscribe"), {"email": valid_email})
        valid_email_response = ajax_subscribe(valid_email_request)
        self.assertEqual(valid_email_response.status_code, 200)
        print(valid_email_response.content)
        self.assertContains(valid_email_response, "OK")
        assert len(responses.calls) == 1

    @responses.activate
    def test_wrong_code(self):
        responses.add(responses.GET, re.compile(r'https://timepad.ru/api/.+'),
                      body='{"error": "bad code"}', status=200,
                      content_type='application/json')

        response = ajax_subscribe(self.request.post(reverse("subscribe"), {"email": 'foo@bar.ru'}))
        self.assertContains(response, 'Failed')
        assert len(responses.calls) == 1

    def test_validate_email(self):
        from apps.meetup.utils import validate_email
        valid_email = "This-is_valid.email@valid.domain-name.tld"
        invalid_emails = ["email with spaces@valid.domain-name.tld",
                          "email@wrong-domain", "AbraCadabra"]

        self.assertTrue(validate_email(valid_email))
        for invalid in invalid_emails:
            self.assertFalse(validate_email(invalid), "Email '{0}' shouldn't be valid".format(invalid))

    @patch.dict('os.environ', clear=True)
    @responses.activate
    def test_subscribe_mail_envfail(self):
        responses.add(responses.GET, re.compile(r'https://timepad.ru/api/.+'),
                      body='Unicorns here', status=500,
                      content_type='application/json')
        from apps.meetup.utils import subscribe_mail
        email = "email@domain.tld"

        self.assertFalse(subscribe_mail(email))
        assert len(responses.calls) == 0
