import requests
import os

client_id = os.environ["CLIENT_ID"]
client_secret = os.environ["CLIENT_SECRET"]
API_URL = "https://oauth.battle.net/token"


def get_wow_token_price(client_id, client_secret):
    token_url = "https://us.battle.net/oauth/token"
    api_url = "https://us.api.blizzard.com/data/wow/token/"

    data = {
        "grant_type": "client_credentials"
    }

    try:
        #Request OAuth access token
        response = requests.post(token_url, auth=(client_id, client_secret), data=data)
        response.raise_for_status()
        access_token = response.json()["access_token"]
        headers = {
            "Authorization": f"Bearer {access_token}"
        }

        params = {
            "namespace": "dynamic-us"
        }
        response = requests.get(api_url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()
        current_price = data["price"]
        return current_price

    except requests.exceptions.RequestException as e:
        print(f"Error retrieving WoW Token price: {e}")

    return None

#I made this because the formatting was butt ugly
def format_price(current_price):
    wow_token_price = get_wow_token_price(client_id, client_secret)
    #Rename these later these are terrible names
    readable_price_1 = str(wow_token_price)[:3].zfill(3)
    readable_price_2 = str(wow_token_price)[3:6].zfill(3)
    final_price = readable_price_1 + ',' + readable_price_2
    if wow_token_price:
        return final_price
    else:
        print("Error retrieving WoW Token price.")
