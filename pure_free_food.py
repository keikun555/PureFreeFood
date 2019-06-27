from googlesearch import search
from bs4 import BeautifulSoup
import json
import requests

class EatClubDish:
    def __init__(self, person, dish_name, restaurant, star_str, star_num, rating_num, description, icons, image_url, address, location):
        self.person = person
        self.dish_name = dish_name
        self.restaurant = restaurant
        self.star_str = star_str
        self.star_num = star_num
        self.rating_num = rating_num
        self.description = description
        self.icons = icons
        self.image_url = image_url
        self.address = address
        self.location = location


def send_message(dish):
    webhook_url = 'https://hooks.slack.com/services/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'
    slack_data = {"blocks": [
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "Hi! *{}* provides a free food!\n\n *Press Reserve button if you want it:*".format(dish.person)
            }
        },
        {
            "type": "divider"
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "*{}* from {}\n{} {}   {} Ratings\n {}\n\n{}"
                    .format(dish.dish_name, dish.restaurant, dish.star_str, dish.star_num, dish.rating_num, dish.description, dish.icons)
            },
            "accessory": {
                "type": "image",
                "image_url": "{}".format(dish.image_url),
                "alt_text": "{}".format(dish.dish_name)
            }
        },
        {
            "type": "divider"
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "Address: *{}*\nLocation: *{}*\n".format(dish.address, dish.location)
            }
        },
        {
            "type": "divider"
        },
        {
            "type": "actions",
            "elements": [
                {
                    "type": "button",
                    "text": {
                        "type": "plain_text",
                        "text": "Reserve!",
                        "emoji": True
                    },
                    "value": "click_me_123"
                }
            ]
        }
    ]}

    response = requests.post(
        webhook_url, data=json.dumps(slack_data),
        headers={'Content-Type': 'application/json'}
    )

    print(response.status_code, response.text)


def search_dish_link(dish_name):
    query = dish_name + " eat club"
    res_url = ""
    for j in search(query, tld="com", num=5, stop=5, pause=2): 
        if "https://www.eatclub.com/s/restaurant/" in j or "https://www.eatclub.com/dish/" in j:
            res_url = j
            break
    if not res_url: return None
    if "https://www.eatclub.com/dish/" in res_url: return res_url
    else:
        response = requests.get(res_url)
        restaurant_soup = BeautifulSoup(response.content, features="html.parser")
        nodes = restaurant_soup.find_all(text=dish_name)
        if not nodes: return None
        return "https://www.eatclub.com" + nodes[0].parent.parent['href']


def get_dish(dish_url, user_dict):
    # response = requests.get(dish_url)
    # print(dish_url)
    # dish_soup = BeautifulSoup(response.content, features="html.parser")
    # print(dish_soup.html)
    # nodes = dish_soup.find_all("span", class_="star-rating")
    # print(nodes[0].text)

    return EatClubDish(
        person="Michael Scott", 
        dish_name=user_dict.get("food"), 
        restaurant=user_dict.get("restaurant"), 
        star_str=":star::star::star::star:", 
        star_num=4.1, 
        rating_num=1113,
        description="3 soft corn tacos served traditionally with grilled chicken, marinated in achiote, Mayan seasoning with dry oregano, black pepper, cumin. They are topped off with cilantro, onion and roasted tomatillo salsa. Enjoy traditional Mexican rice and pinto beans served on the side.",
        icons=":spicy:",
        image_url="https://myeatclub.a.ssl.fastly.net/im/11660/1493159739000/640x460/60/",
        address=user_dict.get("address"),
        location=user_dict.get("location"))


if __name__ == "__main__":
    user_dict = {
        "food": "food",
        "restaurant": "pure",
        "address": "650",
        "location": "K3"
    }
    eat_club_dish = get_dish(search_dish_link("Chicken Katsu Plate"), user_dict)
    send_message(eat_club_dish)