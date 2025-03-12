import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
try:
    import discord
except ImportError:
    raise ImportError("Missing dependency discord.py. Please run `pip install discord.py`.")
import asyncio
from config import DISCORD_BOT_TOKEN, CHANNEL_ID
from commands_user import setup_commands as setup_user_commands  # Import the setup_commands function from commands_user
from commands_admin import setup_admin_commands  # Import the setup_admin_commands function from commands_admin

async def send_command(bot, channel_id, command):
    channel = bot.get_channel(channel_id)
    await channel.send(command)

if __name__ == "__main__":
    bot = discord.Client()
    setup_user_commands(bot)  # Setup user commands
    setup_admin_commands(bot)  # Setup admin commands
    bot.run(DISCORD_BOT_TOKEN)  # Use configured token.
    asyncio.run(send_command(bot, CHANNEL_ID, "!setzip 12345"))