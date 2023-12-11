import os
import requests


client_id = os.environ["CLIENT_ID"]
client_secret = os.environ["CLIENT_SECRET"]


def get_selfie(client_id, client_secret, name, realm):
    token_url = "https://us.battle.net/oauth/token"
    api_url = f"https://us.api.blizzard.com/profile/wow/character/{realm}/{name}/character-media"

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
            "namespace": "profile-us",
            "locale": "en_US"
        }
        response = requests.get(api_url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()
        print(data)
        avatar_url = data["assets"][2]["value"]
        return avatar_url

    except requests.exceptions.RequestException as e:
        print("Error")

    return