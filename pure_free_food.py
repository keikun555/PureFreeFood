from googlesearch import search
from bs4 import BeautifulSoup
import json
import requests


class EatClubDish:
    def __init__(self, dish_name, restaurant, star_str, star_num, rating_num, description, icons, image_url, address, location):
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
                "text": "Hi! There is a free food!\n\n *Press Reserve button if you want it:*"
            }
        },
        {
            "type": "divider"
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "*{}* from {}\n{} {}\n\n{}"
                    .format(dish.dish_name, dish.restaurant,
                            "" if dish.star_num is None else f'{dish.star_str} {dish.star_num}   {dish.rating_num} Ratings\n',
                            dish.description, dish.icons)
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
    if not res_url:
        return None
    if "https://www.eatclub.com/dish/" in res_url:
        return "https://www.eatclub.com/api/items/" + res_url.split("/")[-2] + "/"
    else:
        response = requests.get(res_url)
        restaurant_soup = BeautifulSoup(
            response.content, features="html.parser")
        nodes = restaurant_soup.find_all(text=dish_name)
        if not nodes:
            return None
        return "https://www.eatclub.com/api/items/" + nodes[0].parent.parent['href'].split("/")[-2] + "/"


def get_dish(dish_url, user_dict):
    dish_dict = requests.get(dish_url).json()

    star_str = ""
    rounded_star = None
    rating = dish_dict.get("average_rating")
    if rating is not None:
        rounded_star = round(rating, 1)
        for i in range(round(rating)):
            star_str += ":star:"

    tag_str = ""
    tags = dish_dict.get("tags")
    if tags is not None:
        for tag in tags:
            tag_str += ":{}:".format(tag.get("value_code"))

    return EatClubDish(
        dish_name=user_dict.get("food"),
        restaurant=user_dict.get("restaurant"),
        star_str=star_str,
        star_num=rounded_star,
        rating_num=dish_dict.get("review_count"),
        description=dish_dict.get("description"),
        icons=tag_str,
        image_url=dish_dict.get("photo").get("url"),
        address=user_dict.get("address"),
        location=user_dict.get("location"))


if __name__ == "__main__":
    user_dict = {
        "food": "food",
        "restaurant": "pure",
        "address": "650",
        "location": "K3"
    }
    eat_club_dish = get_dish(search_dish_link(
        "Chicken Tostada Salad"), user_dict)
    send_message(eat_club_dish)
