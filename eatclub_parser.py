#!/usr/bin/env python3
from bs4 import BeautifulSoup
import re


def grab_info(html_text):
    soup = BeautifulSoup(html_text, 'html.parser')
    infos = {}
    for table in soup.find_all('table'):
        if "Your order is ready" in str(table.text):
            infos["address"] = re.findall("at\\s+(.*)", table.text)[0]
        elif "rack-loc" in str(table):
            infos["location"] = table.find('span').text.strip()
        elif table.find('strong'):
            infos["food"] = table.find('strong').text.strip()
            infos["restaurant"] = re.findall("from\\s+(.*)", table.text)[0]
        else:
            pass
    return infos
