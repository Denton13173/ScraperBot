"""
Discord Bot for Monitoring and Extracting Deal Information

This bot is designed to monitor messages in a Discord server and extract deal information based on specific keywords and patterns.
It listens for messages containing the keyword "deal" and uses regular expressions to parse and extract SKU, discount, and price information from the message content.
Valid deals are cached in a dictionary for further processing or reference.

Features:
- Message Monitoring: Continuously listens for new messages in the server.
- Keyword Detection: Identifies potential deal messages by looking for the keyword "deal".
- Data Extraction: Uses regular expressions to extract SKU, discount, and price data from the message content.
- Data Validation: Ensures that the extracted data follows the expected format.
- Caching: Stores valid deals in a dictionary for easy access and management.
- User Feedback: Sends a confirmation message in the channel when a valid deal is found, or an error message if the format is incorrect.

How to Use:
1. Setup: Ensure you have a .env file with your DISCORD_BOT_TOKEN and DISCORD_CHANNEL_ID.
2. Run the Bot: Execute the script to start the bot.
3. Post Messages: Post messages in the server containing deal information in the format:
   Deal! SKU: 12345, Discount: 20%, Price: $19.99
4. Receive Feedback: The bot will respond with a confirmation message if the deal is valid, or an error message if the format is incorrect.

Example:
Post a message in the server:
Deal! SKU: 12345, Discount: 20%, Price: $19.99

The bot will respond:
Deal found! SKU: 12345, Discount: 20%, Price: $19.99
"""

import discord
import logging
from discord.ext import commands
from dotenv import load_dotenv
from validate_deals import validate_deal  # Import the validate_deal function
from embed_extraction import extract_deal_info, extract_deal_info_from_text  # Import the extraction functions
from config import DISCORD_BOT_TOKEN, CHANNEL_ID, ALLOWED_BOT_IDS
from commands_user import setup_commands as setup_user_commands  # Import the setup_commands function from commands_user
from commands_admin import setup_admin_commands  # Import the setup_admin_commands function from commands_admin
from init_db import init_db  # Import the init_db function
from message_formatter import format_deal_message  # Import the format_deal_message function

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize the database
init_db()

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# Define a dictionary to store valid deals
deals = {}

@bot.event
async def on_ready():
    logging.info(f"Logged in as {bot.user}")
    setup_user_commands(bot)  # Setup user commands
    setup_admin_commands(bot)  # Setup admin commands

@bot.event
async def on_message(message):
    # Skip messages from the bot itself
    if message.author.id == bot.user.id:
        return

    # Check if the message is from an allowed bot
    if message.author.bot and message.author.id in ALLOWED_BOT_IDS:
        logging.info(f"Processing message from bot: {message.author.name}")

        # Determine the message format and extract deal information
        if message.embeds:
            embed = message.embeds[0]
            deal_info = extract_deal_info(embed)
        else:
            deal_info = extract_deal_info_from_text(message.content)

        logging.info(f"Extracted deal info: {deal_info}")

        discount = deal_info["discount"]
        price = deal_info["price"]
        original_price = deal_info.get("original_price", price + discount)  # Assuming original price if not provided

        deal = {"discount": discount, "price": price, "original_price": original_price}

        # Validate the deal
        if validate_deal(deal):
            # Check if the deal has already been sent
            if deal_info["sku"] in deals:
                logging.info("Deal already sent. Skipping.")
                return

            # Cache the valid deal
            deals[deal_info["sku"]] = {"discount": discount, "price": price}

            # Send the deal to the designated channel
            channel = bot.get_channel(CHANNEL_ID)
            if channel:
                embed = format_deal_message(deal_info, message)
                await channel.send(embed=embed)
            else:
                logging.error(f"Channel with ID {CHANNEL_ID} not found.")
        else:
            logging.info("Invalid deal data. Please provide valid discount and price.")

    # Ensure command processing
    await bot.process_commands(message)

if __name__ == "__main__":
    bot.run(DISCORD_BOT_TOKEN)