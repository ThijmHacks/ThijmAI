import os
import requests
from dotenv import load_dotenv

import ThijmAI.speaking.speak as sp

load_dotenv()

HA_URL = os.getenv("HA_URL")
API_TOKEN = os.getenv("API_TOKEN")

if not HA_URL or not API_TOKEN:
    print("Error: HA_URL or API_TOKEN is not set in the .env file.")
    exit(1)

headers = {
    "Authorization": f"Bearer {API_TOKEN}",
    "Content-Type": "application/json",
}


def lights(command):
    entity_id = "light.kamer_thijmen"

    if "on" in command:
        off_on = "turn_on"
    if "off" in command:
        off_on = "turn_off"
    else:
        off_on = "turn_on"
    data = {
        "entity_id": entity_id
    }


    response = requests.post(f"{HA_URL}/api/services/light/{off_on}", json=data, headers=headers)

    if response.status_code == 200:
        print("Successfully set the light with color, brightness, and temperature.")
    else:
        print(f"Error: {response.status_code} - {response.text}")