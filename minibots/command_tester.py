import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
try:
    import discord
except ImportError:
    raise ImportError("Missing dependency discord.py. Please run `pip install discord.py`.")
import asyncio
from config import DISCORD_BOT_TOKEN, CHANNEL_ID

async def send_command(bot, channel_id, command):
    channel = bot.get_channel(channel_id)
    await channel.send(command)

if __name__ == "__main__":
    bot = discord.Client()
    bot.run(DISCORD_BOT_TOKEN)  # Use configured token.
    asyncio.run(send_command(bot, CHANNEL_ID, "!setzip 12345"))