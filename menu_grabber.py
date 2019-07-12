import re
import os
import datetime
import requests
import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


CHROMEDRIVER_PATH = './chromedriver'
PAGE_URL = 'https://www.eatclub.com/menu/{}/'
DISHES_URL = 'https://www.eatclub.com/menus/?categorized_menu=true&day={}&menu_type=individual'
LOGIN_URL = 'https://www.eatclub.com/public/api/log-in/'
EMAIL = os.environ['EAT_CLUB_EMAIL']
PASSWORD = os.environ['EAT_CLUB_PASSWORD']

"""
EAT Club will close the access to today's menu after 10:00am
"""


def login_and_jump_to_menu_page(driver):
    email_field = driver.find_element_by_id('email')
    password_field = driver.find_element_by_id('password')
    submit = driver.find_element_by_class_name('login-btn')
    email_field.send_keys(EMAIL)
    password_field.send_keys(PASSWORD)
    submit.click()
    # wait for new page being loaded
    try:
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "selected-date"))
        )
    except Exception as e:
        raise e 


def get_cookie_str():
    login_dict = {
        'email': EMAIL,
        'password': PASSWORD
    }
    resp_header = requests.put(LOGIN_URL, data=login_dict).headers.get('Set-Cookie')
    cookie = re.sub(r'Path=/[,]{0,1}', '', resp_header)
    return cookie


def get_today_dishes(cookie, index):
    url = DISHES_URL.format(index)
    return requests.get(url, headers={'cookie':cookie}).json().get('items').values()


def get_date_index(driver, day_str):
    date_header = driver.find_element_by_css_selector("button.selected-date > div.date-header")
    selected_date = date_header.get_attribute("innerHTML").split('\n')[1].strip().split(' ')[1]
    if selected_date != day_str:
        dates = driver.find_elements_by_css_selector("button.date-display-button")
        index = 1
        for date in dates:
            if day_str in date.find_element_by_css_selector("div.date-header").get_attribute('innerHTML'):
                return index
            index += 1
    else:
        return driver.current_url.split('/')[-2]


def get_menu():
    '''
    Return: {
        'dish-name': {
            'attr1': 'val1',
            ...
        },
        ...
    }
    '''
    now = datetime.datetime.now()
    weekday = now.weekday()
    if weekday not in [0,2,4]:
        print("Wrong day of Eat Club")
        exit(0)

    day_str = "{}/{}".format(now.month, now.day)
    # day_str = "7/17"

    options = Options()
    options.headless = True
    driver = webdriver.Chrome(CHROMEDRIVER_PATH, options=options)
    driver.get('https://www.eatclub.com/menu/')

    try:
        login_and_jump_to_menu_page(driver)
    except Exception as e:
        driver.quit()
        return

    index = get_date_index(driver, day_str)
    if index == None:
        driver.quit()
        raise Exception("Today's menu is expired")

    cookie_str = get_cookie_str()
    items = get_today_dishes(cookie_str, index)
    
    dishes_dict = {}
    for item in items:
        # TODO: reserve needed data
        dishes_dict[item.get('item')] = item

    driver.quit()
    return dishes_dict


if __name__ == "__main__":
    print(json.dumps(get_menu()))
