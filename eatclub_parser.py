#!/usr/bin/env python3
from bs4 import BeautifulSoup
import re


def grab_info(html_text):
    soup = BeautifulSoup(html_text, 'html.parser')
    infos = {}
    if 'www.eatclub.com' not in html_text or 'Lunch is here!' not in html_text:
        return None
    # check for single item menu
    for table in soup.find_all('table', {'style': re.compile('.*width:\\s*600px.*')}):
        if 'Your order is ready' in str(table):
            infos['address'] = re.findall('at\\s+(.*)', table.text)[0].strip()
        elif 'rack-loc' in str(table):
            infos['location'] = table.find('span').text.strip()
        elif table.find('strong'):
            infos['food'] = table.find('strong').text.strip()
            infos['restaurant'] = re.findall(
                'from\\s+(.*)', table.text)[0].strip()
    # get sides if exists
    infos['sides'] = []
    infos['side_locations'] = []
    if 'location' not in infos:
        # probably a multi item menu
        past_address = False  # for relative locations
        for table in soup.find_all('table', {'style': re.compile('.*width:\\s*600px.*')}):
            if past_address:
                food_info = list(filter(lambda s: s not in ['=20', ''], map(
                    lambda s: s.strip(), table.strings)))
            if 'Your order is ready' in str(table):
                past_address = True
        for i in range(0, len(food_info), 2):
            food, loc = food_info[i], food_info[i + 1]
            if '(side)' in food:
                infos['sides'].append(food)
                infos['side_locations'].append(loc)
            else:
                infos['food'] = food
                infos['location'] = loc
    if re.search(r'(anon|anonymous):\s*true', html_text, re.IGNORECASE):
        infos['anonymous'] = True
    else:
        infos['anonymous'] = False
    return infos
