import discord
import asyncio
from config import DISCORD_BOT_TOKEN, CHANNEL_ID

async def send_test_message(bot, channel_id, content):
    channel = bot.get_channel(channel_id)
    await channel.send(content)

if __name__ == "__main__":
    bot = discord.Client()
    bot.run(DISCORD_BOT_TOKEN)
    asyncio.run(send_test_message(bot, CHANNEL_ID, "Test deal message with SKU and discount"))