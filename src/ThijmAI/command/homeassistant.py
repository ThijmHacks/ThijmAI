import os
import re
import requests
from dotenv import load_dotenv
import ThijmAI.speaking.speak as sp  # Your voice feedback module

# Load .env variables
load_dotenv()

HA_URL = os.getenv("HA_URL")
API_TOKEN = os.getenv("API_TOKEN")

if not HA_URL or not API_TOKEN:
    print("Error: HA_URL or API_TOKEN is not set in the .env file.")
    exit(1)

# Auth headers for Home Assistant API
headers = {
    "Authorization": f"Bearer {API_TOKEN}",
    "Content-Type": "application/json",
}

# Optional named colors to RGB
COLOR_MAP = {
    "red": [255, 0, 0],
    "green": [0, 255, 0],
    "blue": [0, 0, 255],
    "yellow": [255, 255, 0],
    "purple": [128, 0, 128],
    "white": [255, 255, 255],
    "orange": [255, 165, 0],
}

# Word-to-number mapping for spot control
WORD_TO_NUM = {
    "one": "1",
    "two": "2",
    "three": "3"
}

def lights(command: str):
    command = command.lower()

    # Default entity
    entity_id = "light.kamer_thijmen"

    # Spot detection: spot 1 or spot one → light.thijmen_spot_1
    match = re.search(r"spot\s*(\d+|one|two|three)", command)
    if match:
        spot = match.group(1)
        spot_number = WORD_TO_NUM.get(spot, spot)  # Convert "one" → "1" etc.
        entity_id = f"light.thijmen_spot_{spot_number}"

    # Start building the data payload
    data = {
        "entity_id": entity_id
    }

    # On/off command detection
    if "off" in command:
        service = "turn_off"
    else:
        service = "turn_on"

    # Brightness (e.g., "set brightness to 100")
    match = re.search(r"brightness\s*(to)?\s*(\d+)", command)
    if match:
        brightness = int(match.group(2))
        brightness = max(0, min(brightness, 255))
        data["brightness"] = brightness

    # Color temperature
    if "warm" in command:
        data["color_temp"] = 300
    elif "cool" in command:
        data["color_temp"] = 500

    # Check for color keywords in command
    for color_name, rgb in COLOR_MAP.items():
        if color_name in command:
            data["rgb_color"] = rgb
            break

    # Send the request to Home Assistant
    response = requests.post(f"{HA_URL}/api/services/light/{service}", json=data, headers=headers)

    if response.status_code == 200:
        print(f"✅ Successfully updated {entity_id}: {command}")
        sp.speak(f"{entity_id.split('.')[-1]} updated.")
    else:
        print(f"❌ Error: {response.status_code} - {response.text}")
        sp.speak("There was an error updating the lights.")
