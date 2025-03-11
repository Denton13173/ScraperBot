import os
try:
    from dotenv import load_dotenv
except ImportError:
    raise ImportError("Missing dependency python-dotenv. Please run `pip install python-dotenv`.")

load_dotenv()

DISCORD_BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")
GUILD_ID = int(os.getenv("GUILD_ID", "0"))
CHANNEL_ID = int(os.getenv("CHANNEL_ID", "0"))
CATEGORY_ID = int(os.getenv("CATEGORY_ID", "0"))
USER_ID = int(os.getenv("USER_ID", "0"))