# coding: utf-8
"""
Invite new people to subscribe to our mailchimp list.

Creates drafts in gmail account to manually check and send.
Each message contains an unique bitly url for fast signup on mailchimp,
with all required fields prefilled.

Recipeints are taken from csv file format (firstname, lastname, email).
Subscribed and people invited in the past are filtered out for the segment
to avoid spamming them.
"""
import csv
import imaplib

from django.core.management.base import BaseCommand, CommandError

from apps.subscribers.invite import prepare_text, create_draft, is_subscribed, is_invited_to_subscribe


class Command(BaseCommand):
    help = 'Прислать приглашение подписаться на рассылку тем кто был на прошлом митапе'

    def add_arguments(self, parser):
        parser.add_argument('--emails-file', type=str)
        parser.add_argument('--imap-login', type=str)
        parser.add_argument('--imap-password', type=str)

    def handle(self, *args, **options):
        self.connection = imaplib.IMAP4_SSL('imap.gmail.com', port=993)
        self.connection.login(options.get('imap_login'), options.get('imap_password'))

        if options.get('emails_file'):
            emails_csv = options.get('emails_file')
        else:
            raise CommandError('Provide either --emails-file')

        attendees = csv.DictReader(open(emails_csv, encoding='utf-8'), fieldnames=('fn', 'ln', 'email'))

        for person in attendees:
            if is_subscribed(person['email']):
                self.stdout.write('Skipping subscribed: %s' % person['email'])
                continue
            if is_invited_to_subscribe(person['email']):
                self.stdout.write('Skipping    invited: %s' % person['email'])
                continue
            self.handle_person(person)

    def handle_person(self, person):
        text = prepare_text(person['email'], person['fn'], person['ln'])
        create_draft(self.connection, person['email'], person['fn'], person['ln'], text)
        self.stdout.write('Writing email for %s' % person['email'])
