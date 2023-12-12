import os
import requests
from PIL import Image
import time

client_id = os.environ["CLIENT_ID"]
client_secret = os.environ["CLIENT_SECRET"]
image_folder = "character_images"


def clear_folder(folder):
    folder_path = folder
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        try:
            if os.path.isfile(file_path):
                os.remove(file_path)
            elif os.path.isdir(file_path):
                os.rmdir(file_path)
        except Exception as e:
            print(f"Error deleting {file_path}: {e}")
    print("Deletion done")


def process_image(image_link, name, realm):
    clear_folder(image_folder)
    # image_link = get_selfie(client_id, client_secret, name, realm)
    im = Image.open(requests.get(image_link, stream=True).raw)
    (left, upper, right, lower) = (350, 150, 1200, 1050)
    im_crop = im.crop((left, upper, right, lower))
    # im_crop.show()
    im_crop.save(f"character_images/{name}{realm}.png", "PNG")
    time.sleep(2)
    final_img = f"character_images/{name}{realm}.png"
    return final_img


def get_selfie(client_id, client_secret, name, realm):
    token_url = "https://us.battle.net/oauth/token"
    api_url = f"https://us.api.blizzard.com/profile/wow/character/{realm}/{name}/character-media"

    data = {
        "grant_type": "client_credentials"
    }

    try:
        # Request OAuth access token
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
        final_img = process_image(avatar_url, name, realm)
        return final_img

    except requests.exceptions.RequestException as e:
        print("Error")

    return
