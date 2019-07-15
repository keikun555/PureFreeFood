'''
Kei Imada
20190627
The email fetcher for PureFreeFood
'''

from __future__ import print_function
import pickle
import os.path
import datetime as dt
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from apiclient import errors
from lxml import html
import base64
import shelve
import email
import pdb
import re

# If modifying these scopes, delete the file token.pickle.
SCOPES = [
    'https://www.googleapis.com/auth/gmail.modify',
    'https://www.googleapis.com/auth/userinfo.email',
    'https://www.googleapis.com/auth/userinfo.profile',
    'openid'
    # Add other requested scopes.
]
# leeway around Noon on when eatclub gets hour food
EATCLUB_LEEWAY = dt.timedelta(hours=1)
# leeway after eatclub arrival for upforgrabber to forward us eatclubs
UPFORGRAB_LEEWAY = dt.timedelta(hours=6)


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
        self.sender_regex = re.compile('(.*) <(.*@purestorage\.com)>')
        self.date_regex = re.compile('^Date: (.*)$')
        # Fri, Jun 28, 2019 at 11:59 AM
        self.eatclub_date_format = '%a, %b %d, %Y at %I:%M %p'
        # Thu, 27 Jun 2019 11:43:27 -0700
        self.forward_date_format1 = '%a, %d %b %Y %X %z (%Z)'
        self.forward_date_format2 = '%a, %d %b %Y %X %z'
        self.read_labels = {'removeLabelIds': ['UNREAD'],
                            'addLabelIds': ['INBOX']}

    def get_unread_message_ids(self):
        """List all Messages of the user's mailbox matching the query.

        Returns:
          List of Message IDs that are unread
        """
        unread_messages = ListMessagesMatchingQuery(
            self.service, 'me', query='is:unread')
        msg_ids = map(lambda m: m['id'], unread_messages)
        return msg_ids

    def get_eatclub_message(self, msg_id):
        """Get a Message and returns a Mime Message if it's an EATClub message.

        Args:
          msg_id: The ID of the Message required.

        Returns:
          A dictionary if the email is from EATClub else None {
            'sender_name' (str): The name of the sender
            'sender_address' (str): The address of the sender
            'html_content' (HTML str): The HTML content of the message in string format
          }
        """
        message = {}  # to return
        # get the mime message
        mime_message = GetMimeMessage(self.service, 'me', msg_id)
        # set send_name and send_address
        sender = mime_message['From']
        print(sender)
        result = self.sender_regex.match(sender)
        if not result:
            print(
                'EmailFetcher.get_eatclub_message: Unable to parse sender %s as Pure Storage account' % sender)
            return None
        message['sender_name'], message['sender_address'] = result.groups()
        # set html_content
        message['html_content'] = None
        for part in mime_message.get_payload():
            if part.get_content_type() == 'text/html':
                if message['html_content'] is None:
                    message['html_content'] = ''
                try:
                    forward_date = dt.datetime.strptime(
                        mime_message['Date'], self.forward_date_format1).replace(tzinfo=None)
                except ValueError:
                    forward_date = dt.datetime.strptime(
                        mime_message['Date'], self.forward_date_format2).replace(tzinfo=None)
                content = part.get_payload()
                if self._is_valid_eatclub_content(content, forward_date):
                    print('EmailFetcher.get_eatclub_message: Found Valid Up for Grabs email!')
                    print(content[:300])
                    message['html_content'] += content
                    break
        if message['html_content'] is None:
            print('EmailFetcher.get_eatclub_message: Content not found')
            return None
        return message

    def _is_valid_eatclub_content(self, content, forward_date):
        ''' Given xml content, determines whether or not it is eatclub content that is time relevant '''
        # check if content is not empty
        if len(content.strip()) <= 0:
            return False
        # check if it is an EAT Club content
        tree = html.fromstring(content)
        if len(tree.xpath('//div/strong[contains(text(), "EAT Club")]')) <= 0:
            return False

        # check if the dates fit the leeways we defined
        dates = list(
            filter(None, map(lambda s: self.date_regex.match(s), tree.xpath('//text()'))))
        if len(dates) <= 0:
            return False
        date = dates[0].groups()[0]  # first one because its in the header
        eatclub_date = dt.datetime.strptime(date, self.eatclub_date_format)
        noon = dt.datetime.combine(dt.datetime.now().date(), dt.time(12))
        if eatclub_date.weekday() not in [0, 2, 4]:
            # not Mon, Wed, or Fri
            return False
        if abs(eatclub_date - noon) > EATCLUB_LEEWAY:
            # past eatclub leeway
            return False
        if forward_date < eatclub_date and forward_date - eatclub_date > UPFORGRAB_LEEWAY:
            # past upforgrab leeway and forward before eatclub (time machine?)
            return False
        return True


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
        print('An error occurred: %s' % error)


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


def GetMimeMessage(service, user_id, msg_id):
    """Get a Message and use it to create a MIME Message.

    Args:
      service: Authorized Gmail API service instance.
      user_id: User's email address. The special value "me"
      can be used to indicate the authenticated user.
      msg_id: The ID of the Message required.

    Returns:
      A MIME Message, consisting of data from Message.
    """
    try:
        message = service.users().messages().get(userId=user_id, id=msg_id,
                                                 format='raw').execute()

        # print('Message snippet: %s' % message['snippet'])

        msg_str = base64.urlsafe_b64decode(message['raw'].encode('ASCII'))

        mime_msg = email.parser.BytesParser().parsebytes(msg_str)

        return mime_msg
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


def CreateMsgLabels():
    """Create object to update labels.

    Returns:
      A label update object.
    """
    return None


def main():
    """Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """
    fetcher = EmailFetcher()
    unread_ids = fetcher.get_unread_message_ids()
    for msg_id in unread_ids:
        msg = fetcher.get_eatclub_message(msg_id)
        if msg:
            print(msg.keys())


if __name__ == '__main__':
    main()
