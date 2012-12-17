# -*- coding: utf-8 -*-
import contextlib
import datetime
from django.test import TestCase
from requests import patch
from meetup.models import Event


@contextlib.contextmanager
def mock_now(dt_value):
    """Context manager for mocking out datetime.now() in unit tests.

    Example:
    with mock_now(datetime.datetime(2011, 2, 3, 10, 11)):
        assert datetime.datetime.now() == datetime.datetime(2011, 2, 3, 10, 11)

    """

    class MockDateTime(datetime.datetime):
        @classmethod
        def now(cls):
            # Create a copy of dt_value.
            return datetime.datetime(
                dt_value.year, dt_value.month, dt_value.day,
                dt_value.hour, dt_value.minute, dt_value.second, dt_value.microsecond,
                dt_value.tzinfo
            )
    real_datetime = datetime.datetime
    datetime.datetime = MockDateTime
    try:
        yield datetime.datetime
    finally:
        datetime.datetime = real_datetime


class TestOnAir(TestCase):

    def setUp(self):
        self.seventh_meetup = Event(date=datetime.datetime(2012, 11, 21, 19, 0, 0))

    def test_simple(self):

        with mock_now(datetime.datetime(2012, 11, 13, 19, 45)):
            self.assertFalse(self.seventh_meetup.on_air)

        with mock_now(datetime.datetime(2012, 11, 21, 18, 29, 59)):
            self.assertFalse(self.seventh_meetup.on_air)

        with mock_now(datetime.datetime(2012, 11, 21, 18, 30, 0)):
            self.assertTrue(self.seventh_meetup.on_air)

        with mock_now(datetime.datetime(2012, 11, 21, 19, 0, 0)):
            self.assertTrue(self.seventh_meetup.on_air)

        with mock_now(datetime.datetime(2012, 11, 21, 23, 0, 0)):
            self.assertTrue(self.seventh_meetup.on_air)

        with mock_now(datetime.datetime(2012, 11, 21, 23, 0, 1)):
            self.assertFalse(self.seventh_meetup.on_air)

        with mock_now(datetime.datetime(2012, 11, 22, 19, 45, 1)):
            self.assertFalse(self.seventh_meetup.on_air)