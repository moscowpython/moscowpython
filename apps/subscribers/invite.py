# coding: utf-8
import csv
import email
from email.header import Header
from email.utils import formataddr
import glob
import imaplib
from urllib.parse import urlencode
import time
import os

from bitly_api import Connection
from django.template.loader import render_to_string
import mailchimp


mailchimp_api = mailchimp.Mailchimp(os.environ.get('MAILCHIMP_API_KEY'))

invited_emails = None


def is_subscribed(email_address):
    result = mailchimp_api.helper.search_members(email_address)
    return result['exact_matches']['total']


def is_invited_to_subscribe(email_address):
    global invited_emails

    if invited_emails is None:
        invited_emails = set()
        for emails_csv in glob.glob('data/meetup*.csv'):
            old_meetup_attendees = csv.DictReader(open(emails_csv, encoding='utf-8'), fieldnames=('fn', 'ln', 'email'))
            invited_emails |= set(row['email'].lower().strip() for row in old_meetup_attendees)
    return email_address.lower().strip() in invited_emails


def shorten_url(url):
    c = Connection(login=os.environ.get('BITLY_LOGIN'),
                   api_key=os.environ.get('BITLY_API_KEY'))
    return c.shorten(url)['url']


def prepare_text(email_address, first_name, last_name):
    url = 'http://moscowdjango.us10.list-manage1.com/subscribe?' + urlencode({
        'u': 'c697064155714e24c8be7e9d8',
        'id': 'b99c780cc6',
        'EMAIL': email_address,
        'MERGE1': first_name,
        'MERGE2': last_name
    })
    template = render_to_string('subscribers/invite.html', {
        'email': email_address,
        'first_name': first_name,
        'last_name': last_name,
        'url': shorten_url(url)
    })
    return template


def create_draft(connection, email_address, first_name, last_name, text):
    eml = email.message_from_string(text)
    eml['subject'] = 'Приглашение подписаться на рассылку MoscowDjango'
    eml['to'] = formataddr((str(Header('%s %s' % (first_name, last_name), 'utf-8')), email_address))

    return connection.append(
        '"[Google Mail]/Drafts"',
        r'',
        imaplib.Time2Internaldate(time.time()),
        str(eml).encode('utf-8'))
