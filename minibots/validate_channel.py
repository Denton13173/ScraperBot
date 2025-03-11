import discord
import asyncio
from config import DISCORD_BOT_TOKEN, GUILD_ID

async def validate_channel(bot, guild_id, channel_name):
    guild = bot.get_guild(guild_id)
    channel = discord.utils.get(guild.channels, name=channel_name)
    if not channel:
        await guild.create_text_channel(channel_name)
        print(f"Channel '{channel_name}' created.")
    else:
        print(f"Channel '{channel_name}' already exists.")

# Custom client to run validate_channel upon ready.
class MyClient(discord.Client):
    async def on_ready(self):
        await validate_channel(self, GUILD_ID, "deals")

if __name__ == "__main__":
    bot = MyClient()
    bot.run(DISCORD_BOT_TOKEN)  # Use configured token.