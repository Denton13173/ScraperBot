import discord
import os
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

TOKEN = os.getenv("DISCORD_BOT_TOKEN")  # Loads from an environment variable

intents = discord.Intents.default()
intents.message_content = True  # Required to read messages
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

bot.run(TOKEN)