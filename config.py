import os
from dotenv import load_dotenv

load_dotenv()

DISCORD_BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")
CHANNEL_ID = int(os.getenv("DISCORD_CHANNEL_ID"))
ALLOWED_BOT_IDS = {int(bot_id) for bot_id in os.getenv("ALLOWED_BOT_IDS").split(',')}