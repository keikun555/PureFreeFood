'''
Kei Imada
20190627
Main loop for our PureFreeFood app
'''

import time
from eatclub_parser import grab_info as parse_msg
from email_fetcher import EmailFetcher


def main():
    fetcher = EmailFetcher()
    while True:
        print('checking for new messages...')
        unread_message_ids = fetcher.get_unread_message_ids()
        for msg_id in unread_message_ids:
            msg_content = fetcher.get_message(msg_id)
            parsed_msg = parse_msg(msg_content)
            print('NEW MESSAGE')
            print(parsed_msg)
            fetcher.mark_message_read(msg_id)
        time.sleep(10)


if __name__ == '__main__':
    main()
