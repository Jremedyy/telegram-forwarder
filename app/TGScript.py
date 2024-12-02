import os
import requests
from telethon.sync import TelegramClient
from dotenv import load_dotenv
from telethon import TelegramClient, events
from telethon.sessions import StringSession

# Load .env file
load_dotenv()

# Telegram API credentials from .env
print(f"STRING_SESSION: {os.getenv('TELEGRAM_API_ID')}")
API_ID = int(os.getenv("TELEGRAM_API_ID"))
API_HASH = os.getenv("TELEGRAM_API_HASH")
STRING_SESSION = os.getenv("STRING_SESSION_KEY")
if not API_ID or not API_HASH:
    raise ValueError("Missing required environment variables.")


print(f"BOOTING UP!")



# Initialize Telegram client
client = TelegramClient(StringSession(STRING_SESSION), API_ID, API_HASH)

# Mapping of Telegram channels to Discord webhooks
channel_to_webhook = {
    'PowsGemCalls': os.getenv("POW_GEM_CALLS_WEBHOOK"),
}

# Function to create dynamic handlers
def setup_event_handlers(client, mapping):
    for channel_username, webhook_url in mapping.items():
        print(f"now listening to: {channel_username}")
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
print("Connecting to Telegram...")
client.start()
print("Connected to Telegram!")
client.run_until_disconnected()
