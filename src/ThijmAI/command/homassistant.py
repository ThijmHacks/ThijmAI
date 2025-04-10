import os
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get Home Assistant URL and API Token from environment variables
HA_URL = os.getenv("HA_URL")
API_TOKEN = os.getenv("API_TOKEN")

# Check if the variables are loaded correctly
if not HA_URL or not API_TOKEN:
    print("Error: HA_URL or API_TOKEN is not set in the .env file.")
    exit(1)

# Define headers for authentication
headers = {
    "Authorization": f"Bearer {API_TOKEN}",
    "Content-Type": "application/json",
}

# Example: Turn on the light (replace with the correct entity_id)
entity_id = "light.kamer_thijmen"

# Data to send for turning on the light
data = {
    "entity_id": entity_id
}

# Send the request to turn on the light
response = requests.post(f"{HA_URL}/api/services/light/turn_off", json=data, headers=headers)

if response.status_code == 200:
    print(f"Successfully turned on {entity_id}")
else:
    print(f"Error: {response.status_code} - {response.text}")
