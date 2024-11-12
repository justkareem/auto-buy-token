import os

import requests
import time

# Telegram bot configuration (set as environment variables)
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# API endpoint to fetch the list of coins
params = {
    "offset": 0,
    "limit": 10,
    "includeNsfw": "true"
}

# Creator filter
TARGET_CREATOR = "EZX7c1hARBCiVTY62EJLEPwVsUaZWhmvKkuW3nxexidY"

url = f"https://frontend-api.pump.fun/coins/user-created-coins/{TARGET_CREATOR}"


# Function to send messages to Telegram
def send_telegram_message(message):
    telegram_url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "HTML"
    }
    response = requests.post(telegram_url, data=payload)
    return response.json()


# Function to fetch and process new coin listings
def fetch_and_notify_new_coins(last_checked_timestamp):
    response = requests.get(url, params=params)
    data = response.json()

    for coin in data:
        # Check if the coin was created after the last checked timestamp and by the target creator
        if coin["created_timestamp"] > last_checked_timestamp and coin["creator"] == TARGET_CREATOR:
            # Build message to send
            message = (
                f"🔹 <b>New Coin Listed!</b>\n"
                f"<b>Name:</b> {coin['name']}\n"
                f"<b>Symbol:</b> {coin['symbol']}\n"
                f"<b>Description:</b> {coin['description']}\n"
                f"<b>Market Cap:</b> ${coin['usd_market_cap']}\n"
                f"<b>Website:</b> {coin.get('website', 'N/A')}\n"
                f"<b>Twitter:</b> {coin.get('twitter', 'N/A')}\n"
                f"<b>Telegram:</b> {coin.get('telegram', 'N/A')}\n"
                f"<b>Image:</b> {coin.get('image_uri', 'N/A')}\n"
                f"<b>More Info:</b> https://pump.fun/coin/{coin['mint']}\n"
            )
            send_telegram_message(message)
            print("Sent message for:", coin["name"])


# Main loop to poll for new coins
last_checked_timestamp = int(time.time() * 1000)  # Initialize with the current timestamp

while True:
    fetch_and_notify_new_coins(last_checked_timestamp)
    # Update the last checked timestamp to the most recent coin's created timestamp
    last_checked_timestamp = int(time.time() * 1000)
    # Wait before polling again
    time.sleep(5)  # Poll every 5 seconds
