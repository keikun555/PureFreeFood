from googlesearch import search
from bs4 import BeautifulSoup
import json
import requests


class EatClubDish:
    def __init__(self, dish_name, restaurant, star_str, star_num,
                 rating_num, description, icons, image_url, page_url, address,
                 location, sides, side_locations, sender):
        self.dish_name = dish_name
        self.restaurant = restaurant
        self.star_str = star_str
        self.star_num = star_num
        self.rating_num = rating_num
        self.description = description
        self.icons = icons
        self.image_url = image_url
        self.page_url = page_url
        self.address = address
        self.location = location
        self.sides = sides
        self.side_locations = side_locations
        self.sender = sender


def send_message(dish):
    webhook_url = 'https://hooks.slack.com/services/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'
    title = "Go grab" if dish.sender is None else dish.sender + " shares"
    dish_loc = "Address: *{}*\nLocation: *{}*".format(dish.address, dish.location)
    sides_str = "No sides"

    for i in range(len(dish.sides)):
        sides_str += "{}\nLocation: *{}*\n".format(
            dish.sides[i], dish.side_locations[i])

    slack_data = {"blocks": [
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "{} a free food!".format(title)
                # *Press Reserve button if you want it:*"
            }
        },
        {
            "type": "divider"
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "*<{}|{}>* from {}\n{} {}\n\n{}\n{}"
                    .format(dish.page_url, dish.dish_name, dish.restaurant,
                            "" if dish.star_num is None else f'{dish.star_str} {dish.star_num}   {dish.rating_num} Ratings\n',
                            dish.description, dish.icons, dish_loc)
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
                "text": "{}".format(sides_str)
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
    api_url_prefix = "https://www.eatclub.com/api/items/"
    page_url_prefix = "https://www.eatclub.com/dish/"
    query = dish_name + " eat club"
    res_url = ""
    for j in search(query, tld="com", num=5, stop=5, pause=2):
        if "https://www.eatclub.com/s/restaurant/" in j or "https://www.eatclub.com/dish/" in j:
            res_url = j
            break
    if not res_url:
        return None, None
    if page_url_prefix in res_url:
        return api_url_prefix + res_url.split("/")[-2] + "/", res_url
    else:
        response = requests.get(res_url)
        restaurant_soup = BeautifulSoup(
            response.content, features="html.parser")
        nodes = restaurant_soup.find_all(text=dish_name)
        if not nodes:
            return None, None
        dish_suffix = nodes[0].parent.parent['href']
        page_url = page_url_prefix + dish_suffix
        return api_url_prefix + dish_suffix.split("/")[-2] + "/", page_url


def get_dish(dish_url, page_url, user_dict):
    return EatClubDish(
        dish_name='Mandarin Citrus Chicken with Rice',
        restaurant='Kung Pao Kitchen',
        star_str=':star:' * round(3.6),
        star_num=3.6,
        rating_num=456,
        description='A simple Chinese-American trio of sweet and tangy citrus chicken. Served with jasmine rice and sauteed vegetables.',
        icons=':dairy_free:',
        image_url='https://myeatclub.a.ssl.fastly.net/im/16393/1551895001000/600x600/60/',
        page_url='www.google.com',
        address='650 Castro Street 4th Floor',
        location='L2',
        sides=[],
        side_locations=[],
        sender='Kei Imada'
    )
    dish_dict = requests.get(dish_url).json()

    # stars
    star_str = ""
    rounded_star = None
    rating = dish_dict.get("average_rating")
    if rating is not None:
        rounded_star = round(rating, 1)
        for i in range(round(rating)):
            star_str += ":star:"

    # tags
    tag_str = ""
    tags = dish_dict.get("tags")
    if tags is not None:
        for tag in tags:
            tag_str += ":{}:".format(tag.get("value_code"))

    # sides
    sides = user_dict.get("sides")
    side_locations = user_dict.get("side_locations")

    # sender
    sender = None
    if not user_dict.get("anonymous"):
        sender = user_dict.get("sender_name")

    return EatClubDish(
        dish_name=user_dict.get("food"),
        restaurant=user_dict.get("restaurant"),
        star_str=star_str,
        star_num=rounded_star,
        rating_num=dish_dict.get("review_count"),
        description=dish_dict.get("description"),
        icons=tag_str,
        image_url=dish_dict.get("photo").get("url"),
        page_url=page_url,
        address=user_dict.get("address"),
        location=user_dict.get("location"),
        sides=sides,
        side_locations=side_locations,
        sender=sender)


if __name__ == "__main__":
    user_dict = {
        "food": "food",
        "restaurant": "pure",
        "address": "650",
        "location": "K3",
        "anonymous": False,
        "sender_name": "Mike",
        "sides": [],
        "side_locations": []
    }
    dish_dict, page_url = search_dish_link("Chicken Tostada Salad")
    eat_club_dish = get_dish(dish_dict, page_url, user_dict)
    send_message(eat_club_dish)
