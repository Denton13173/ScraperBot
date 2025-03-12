import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("DISCORD_BOT_TOKEN")
GUILD_ID = int(os.getenv("DISCORD_GUILD_ID"))  # Add your guild ID to the .env file

# Validate that .env is loaded correctly
print(f"Token loaded: {TOKEN is not None}")

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# Define user_prefs dictionary to store user preferences
user_prefs = {}

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    guild = discord.utils.get(bot.guilds, id=GUILD_ID)
    if guild:
        print(f"Bot is in the server: {guild.name} (ID: {guild.id})")
        await check_commands(guild)
    else:
        print("Bot is not in the specified server.")

async def check_commands(guild):
    required_commands = ["setzip", "checkzip"]
    existing_commands = [command.name for command in bot.commands]
    missing_commands = [cmd for cmd in required_commands if cmd not in existing_commands]

    if not missing_commands:
        print("All required commands are present.")
    else:
        print(f"Missing commands: {', '.join(missing_commands)}")

@bot.command()
async def setzip(ctx, zip_code):
    user_id = ctx.author.id
    user_prefs[user_id] = zip_code
    await ctx.send(f"ZIP code set to {zip_code}")

@bot.command()
async def checkzip(ctx):
    user_id = ctx.author.id
    zip_code = user_prefs.get(user_id, "not set")
    await ctx.send(f"Your ZIP code is {zip_code}")

if __name__ == "__main__":
    bot.run(TOKEN)