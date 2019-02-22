"""GMail Client Ability

This module contains the ``GMailClientAbility`` class, which represents a
user's ability to retrieve emails from their GMail account.
"""

import base64
import email
import logging
import pickle
import pprint
import os.path

from apiclient import errors
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import mailparser


logger = logging.getLogger('tsbc-nc-user.gmail-client')


# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']


class GMailError(Exception):
    """GMail-specific exception."""


class GMailClient:

    def __init__(self, **kargs):
        self._service = None

    @property
    def service(self):
        """Returns a GMail Service instance for accessing the GMail API. Assumes a
        gmail credentials JSON file at secrets/gmail-credentials.json.
        """
        if self._service:
            return self._service
        creds = None
        # The file token.pickle stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists('secrets/gmail-token.pickle'):
            with open('secrets/gmail-token.pickle', 'rb') as token:
                creds = pickle.load(token)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'secrets/gmail-credentials.json', SCOPES)
                creds = flow.run_local_server()
            # Save the credentials for the next run
            with open('secrets/gmail-token.pickle', 'wb') as token:
                pickle.dump(creds, token)
        self._service = build('gmail', 'v1', credentials=creds)
        return self._service

    def get_messages_matching_query(self, query=''):
        """List all Messages of the user's mailbox matching the query.

        Args:
            query: String used to filter messages returned.
                Eg.- 'from:user@some_domain.com' for Messages from a particular
                sender.

        Returns:
            List of Messages that match the criteria of the query. Note that the
            returned list contains Message IDs, you must use get with the
            appropriate ID to get the details of a Message.
        """
        try:
            response = self.service.users().messages().list(
                userId='me', q=query).execute()
            messages = []
            if 'messages' in response:
                messages.extend(response['messages'])
            while 'nextPageToken' in response:
                page_token = response['nextPageToken']
                response = self.service.users().messages().list(
                    userId='me',
                    q=query,
                    pageToken=page_token).execute()
                messages.extend(response['messages'])
            return messages
        except errors.HttpError as error:
            raise GMailError(f'An error occurred: {error}')

    def get_message(self, msg_id):
        """Get a Message with given ID.

        Args:
            msg_id: The ID of the Message required.

        Returns:
            A Message.
        """
        try:
            message = self.service.users().messages().get(
                userId='me', id=msg_id).execute()
            return message
        except errors.HttpError as error:
            raise GMailError(f'An error occurred: {error}')

    def fetch_message_bytes(self, msg_id):
        """Fetch a Message and return its bytes.

        Args:
            msg_id: The ID of the Message required.

        Returns:
            A bytes string b'...'.
        """
        try:
            message = self.service.users().messages().get(
                userId='me',
                id=msg_id,
                format='raw').execute()
            return base64.urlsafe_b64decode(message['raw'].encode('ASCII'))
        except errors.HttpError as error:
            raise GMailError(f'An error occurred: {error}')

    @staticmethod
    def get_message_mail_instance(message_bytes):
        return mailparser.parse_from_bytes(message_bytes)

    def get_html_message_matching_query(self, query=''):
        try:
            messages = self.get_messages_matching_query(query=query)
            msg_id = messages[0]['id']
            message_bytes = self.fetch_message_bytes(msg_id)
            mail = self.get_message_mail_instance(message_bytes)
            return mail.text_html[0]
        except IndexError:
            raise GMailError(
                f'Failed to fetch the first GMail message matching query'
                f' "{query}".')


if __name__ == '__main__':
    print(GMailClient().get_html_message_matching_query(
        query='from:tsbcdev@gmail.com'))
