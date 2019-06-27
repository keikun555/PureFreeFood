'''
Kei Imada
20190627
The email fetcher for PureFreeFood
'''

from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from apiclient import errors
import base64
import shelve

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']


class EmailFetcher(object):
    ''' fetches emails '''

    def __init__(self):
        creds = None
        # The file token.pickle stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                creds = flow.run_local_server()
            # Save the credentials for the next run
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)

        self.service = build('gmail', 'v1', credentials=creds)
        self.msg_id_db = shelve.open('msg_id_shelf')

    def __del__(self):
        self.msg_id_db.close()

    def get_unread_message_ids(self):
        """List all Messages of the user's mailbox matching the query.

        Returns:
          List of Message IDs that are unread
        """
        unread_messages = ListMessagesMatchingQuery(
            self.service, 'me', query='is:unread')
        msg_ids = map(lambda m: m['id'], unread_messages)
        return filter(lambda key: key not in self.msg_id_db, msg_ids)

    def get_message(self, msg_id):
        """Get a Message and returns a HTML Message.

        Args:
          msg_id: The ID of the Message required.

        Returns:
          A HTML Message, consisting of data from Message.
        """
        return GetHTMLMessage(self.service, 'me', msg_id)

    def mark_message_read(self, msg_id):
        """Marks the given Message unread.

        Args:
          msg_id: The id of the message to mark unread.
        """
        self.msg_id_db[msg_id] = True
        self.msg_id_db.sync()


def ListMessagesMatchingQuery(service, user_id, query=''):
    """List all Messages of the user's mailbox matching the query.

    Args:
      service: Authorized Gmail API service instance.
      user_id: User's email address. The special value "me"
      can be used to indicate the authenticated user.
      query: String used to filter messages returned.
      Eg.- 'from:user@some_domain.com' for Messages from a particular sender.

    Returns:
      List of Messages that match the criteria of the query. Note that the
      returned list contains Message IDs, you must use get with the
      appropriate ID to get the details of a Message.
    """
    try:
        response = service.users().messages().list(userId=user_id,
                                                   q=query).execute()
        messages = []
        if 'messages' in response:
            messages.extend(response['messages'])

        while 'nextPageToken' in response:
            page_token = response['nextPageToken']
            response = service.users().messages().list(userId=user_id, q=query,
                                                       pageToken=page_token).execute()
            messages.extend(response['messages'])

        return messages
    except errors.HttpError as error:
        print ('An error occurred: %s' % error)


def GetHTMLMessage(service, user_id, msg_id):
    """Get a Message and use it to create a HTML Message.

    Args:
      service: Authorized Gmail API service instance.
      user_id: User's email address. The special value "me"
      can be used to indicate the authenticated user.
      msg_id: The ID of the Message required.

    Returns:
      A HTML Message, consisting of data from Message.
    """
    try:
        message = service.users().messages().get(userId=user_id, id=msg_id,
                                                 format='raw').execute()

        msg_str = base64.urlsafe_b64decode(message['raw'].encode('ASCII'))

        return msg_str
    except errors.HttpError as error:
        print('An error occurred: %s' % error)


def ModifyMessage(service, user_id, msg_id, msg_labels):
    """Modify the Labels on the given Message.

    Args:
      service: Authorized Gmail API service instance.
      user_id: User's email address. The special value "me"
      can be used to indicate the authenticated user.
      msg_id: The id of the message required.
      msg_labels: The change in labels.

    Returns:
      Modified message, containing updated labelIds, id and threadId.
    """
    try:
        message = service.users().messages().modify(userId=user_id, id=msg_id,
                                                    body=msg_labels).execute()

        label_ids = message['labelIds']

        print('Message ID: %s - With Label IDs %s' % (msg_id, label_ids))
        return message
    except errors.HttpError as error:
        print('An error occurred: %s' % error)


def main():
    """Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server()
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('gmail', 'v1', credentials=creds)

    # Call the Gmail API
    unread_messages = ListMessagesMatchingQuery(
        service, 'me', query='is:unread')
    for msg in unread_messages:
        print(GetHTMLMessage(service, 'me', msg['id']))


if __name__ == '__main__':
    main()
