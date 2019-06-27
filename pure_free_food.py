from googlesearch import search
from bs4 import BeautifulSoup
import json
import requests

def send_message():
    webhook_url = 'https://hooks.slack.com/services/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'
    slack_data = {"blocks": [
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "Hello, Assistant to the Regional Manager Dwight! *Michael Scott* wants to know where you'd like to take the Paper Company investors to dinner tonight.\n\n *Please select a restaurant:*"
            }
        },
        {
            "type": "divider"
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "*Farmhouse Thai Cuisine*\n:star::star::star::star: 1528 reviews\n They do have some vegan options, like the roti and curry, plus they have a ton of salad stuff and noodles can be ordered without meat!! They have something for everyone here"
            },
            "accessory": {
                "type": "image",
                "image_url": "https://s3-media3.fl.yelpcdn.com/bphoto/c7ed05m9lC2EmA3Aruue7A/o.jpg",
                "alt_text": "alt text for image"
            }
        },
        { 
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "*Ler Ros*\n:star::star::star::star: 2082 reviews\n I would really recommend the  Yum Koh Moo Yang - Spicy lime dressing and roasted quick marinated pork shoulder, basil leaves, chili & rice powder."
            },
            "accessory": {
                "type": "image",
                "image_url": "https://s3-media2.fl.yelpcdn.com/bphoto/DawwNigKJ2ckPeDeDM7jAg/o.jpg",
                "alt_text": "alt text for image"
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
                        "text": "Farmhouse",
                        "emoji": True
                    },
                    "value": "click_me_123"
                },
                {
                    "type": "button",
                    "text": {
                        "type": "plain_text",
                        "text": "Kin Khao",
                        "emoji": True
                    },
                    "value": "click_me_123"
                },
                {
                    "type": "button",
                    "text": {
                        "type": "plain_text",
                        "text": "Ler Ros",
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

if __name__ == "__main__":
    print(search_dish_link("Chicken Katsu Plate"))