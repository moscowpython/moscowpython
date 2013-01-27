# -*- coding: utf-8 -*-
import logging
import os
import requests
import sys

from django.core.exceptions import ValidationError
from django.core.validators import validate_email as _validate_email


logger = logging.getLogger('subscribe')


def validate_email(email):
    try:
        _validate_email(email)
        return True
    except ValidationError:
        return False


def subscribe_mail(email):
    """ Subscribe user via Timepad

        Docs: https://github.com/timepad/timepad_api/wiki/%D0%94%D0%BE%D0%B1%D0%B0%D0%B2%D0%BB%D0%B5%D0%BD%D0%B8%D0%B5-%D0%B0%D0%B4%D1%80%D0%B5%D1%81%D0%BE%D0%B2-%D0%B2-%D1%81%D0%BF%D0%B8%D1%81%D0%BE%D0%BA-%D1%80%D0%B0%D1%81%D1%81%D1%8B%D0%BB%D0%BA%D0%B8
    """
    try:
        payload = {
            'code': os.environ['TIMEPAD_API_KEY'],
            'id': os.environ['TIMEPAD_ORG_ID'],
            'm_id': os.environ['TIMEPAD_MAILLIST_ID'],
            'i0_email': email
        }
    except KeyError as e:
        logger.error('Can not subscribe, missing key %s' % e)
        return False

    try:
        my_config = {'verbose': sys.stderr}
        response = requests.get('http://timepad.ru/api/maillist_add_items/', params=payload, config=my_config)
    except requests.RequestException:
        logger.error('Timepad is unavailable')
        return False

    try:
        return response.status_code == 200 and response.json['result'] == 'ok'
    except KeyError:
        return False
