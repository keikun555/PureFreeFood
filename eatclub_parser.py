#!/usr/bin/env python3
from bs4 import BeautifulSoup
import re


def grab_info(html_text):
    soup = BeautifulSoup(html_text, 'html.parser')
    infos = {}
    if "www.eatclub.com" not in html_text:
        return None
    for table in soup.find_all('table'):
        if "Your order is ready" in str(table):
            infos["address"] = re.findall("at\\s+(.*)", table.text)[0].strip()
        elif "rack-loc" in str(table):
            infos["location"] = table.find('span').text.strip()
        elif table.find('strong'):
            infos["food"] = table.find('strong').text.strip()
            infos["restaurant"] = re.findall("from\\s+(.*)", table.text)[0].strip()
        else:
            pass
    return infos

