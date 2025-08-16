"""
Fetches all LinkedIn Ad Library entries for a given advertiser and saves them to a JSON file.
Handles pagination, basic retry logic, and rate limiting.
"""

import os
import time
import json
import requests
from dotenv import load_dotenv

load_dotenv()

ACCESS_TOKEN = os.getenv('LI_ACCESS_TOKEN')
if not ACCESS_TOKEN:
    raise ValueError("Missing LI_ACCESS_TOKEN in .env file.")

BASE_URL = "https://api.linkedin.com/rest/adLibrary"
ADVERTISER_NAME = "airbnb"  # Change this to target a different advertiser

headers = {
    "Authorization": f"Bearer {ACCESS_TOKEN}",
    "LinkedIn-Version": "202507",
    "X-Restli-Protocol-Version": "2.0.0",
    "Content-Type": "application/json"
}

start = 0
count = 25
all_data = []
max_retries = 5
stop_fetching = False

while not stop_fetching:
    params = {
        "advertiser": ADVERTISER_NAME,
        "q": "criteria",
        "start": start,
        "count": count,
    }

    retries = 0
    while retries <= max_retries:
        response = requests.get(BASE_URL, headers=headers, params=params)

        if response.status_code == 200:
            data = response.json()
            elements = data.get("elements", [])

            if not elements:
                stop_fetching = True
                break

            all_data.extend(elements)
            start += count
            time.sleep(5)  # Respect rate limits
            break

        elif response.status_code == 429:  # Rate limited
            wait_time = 2 ** retries
            time.sleep(wait_time)
            retries += 1
        else:  # Any other error
            stop_fetching = True
            break
    else:
        break

with open("airbnb_all_ads.json", "w", encoding="utf-8") as f:
    json.dump(all_data, f, ensure_ascii=False, indent=4)
