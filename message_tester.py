import discord
import asyncio
from config import DISCORD_BOT_TOKEN, CHANNEL_ID
from commands_user import setup_commands as setup_user_commands  # Import the setup_commands function from commands_user
from commands_admin import setup_admin_commands  # Import the setup_admin_commands function from commands_admin

async def send_test_message(bot, channel_id, content):
    channel = bot.get_channel(channel_id)
    await channel.send(content)

if __name__ == "__main__":
    bot = discord.Client()
    setup_user_commands(bot)  # Setup user commands
    setup_admin_commands(bot)  # Setup admin commands
    bot.run(DISCORD_BOT_TOKEN)
    asyncio.run(send_test_message(bot, CHANNEL_ID, "Test deal message with SKU and discount"))