import os
from dotenv import load_dotenv
from telethon import TelegramClient, events
import requests

# Load .env file
load_dotenv()

# Telegram API credentials from .env
API_ID = int(os.getenv("TELEGRAM_API_ID"))
API_HASH = os.getenv("TELEGRAM_API_HASH")

# Initialize Telegram client
client = TelegramClient('session_name', API_ID, API_HASH)

# Mapping of Telegram channels to Discord webhooks
channel_to_webhook = {
    'PowsGemCalls': os.getenv("POW_GEM_CALLS_WEBHOOK"),
}

# Function to create dynamic handlers
def setup_event_handlers(client, mapping):
    for channel_username, webhook_url in mapping.items():
        @client.on(events.NewMessage(chats=channel_username))
        async def handler(event, webhook_url=webhook_url):
            # Get the message text
            message = event.raw_text
            print(f"New message from {channel_username}: {message}")

            # Forward the message to the Discord webhook
            response = requests.post(webhook_url, json={"content": message})
            if response.status_code == 204:
                print(f"Message forwarded to Discord successfully: {channel_username}")
            else:
                print(f"Failed to forward message to Discord: {response.status_code}, {response.text}")

# Set up event handlers dynamically
setup_event_handlers(client, channel_to_webhook)

# Start the Telegram client
client.start()
client.run_until_disconnected()
