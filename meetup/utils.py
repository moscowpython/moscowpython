# -*- coding: utf-8 -*-
import requests


def subscribe_mail(email):
    response = requests.post('http://moscowdjango.timepad.ru/org/subscribe', data={'email': email})
    if response.status_code == 200 and u'Вы подписались' in response.text:
        return True
    else:
        return False