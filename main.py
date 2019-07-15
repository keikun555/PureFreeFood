'''
Kei Imada
20190627
Main loop for our PureFreeFood app
'''

import time
import datetime as dt
from eatclub_parser import grab_info as parse_msg
from email_fetcher import EmailFetcher
import pure_free_food as pff


def main():
    fetcher = EmailFetcher()
    now = dt.datetime.now()
    if now.weekday() not in [0, 2, 4]:
        # not EAT Club weekday
        return
    noon = dt.datetime.combine(now.date(), dt.time(12))
    while abs(now - noon) <= dt.timedelta(house=6):
        # from 6:00 AM to 6:00 PM
        print('checking for new messages...')
        unread_message_ids = fetcher.get_unread_message_ids()
        for msg_id in unread_message_ids:
            message = fetcher.get_eatclub_message(msg_id)
            if message is not None:
                # if it is a Up for Grab message
                parsed_msg = parse_msg(message['html_content'])
                parsed_msg['sender_name'] = message['sender_name']
                parsed_msg['sender_address'] = message['sender_address']
                print('NEW MESSAGE')
                print(parsed_msg)
                dish_dict, page_url = pff.search_dish_link(parsed_msg.get("food"))
                eat_club_dish = pff.get_dish(dish_dict, page_url, parsed_msg)
                pff.send_message(eat_club_dish)
            fetcher.mark_message_read(msg_id)
        time.sleep(10)


if __name__ == '__main__':
    main()
