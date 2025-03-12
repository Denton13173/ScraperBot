"""
TODO: Review and Implement Missing Commands

1. !addfilter 
   - Description: Add a new keyword to the filters.
   - Missing: Implementation logic to add the keyword to the filter list.
   - Plan: Implement logic to store the keyword in a persistent storage (e.g., database or in-memory list).

2. !removefilter
   - Description: Remove an existing keyword from the filters.
   - Missing: Implementation logic to remove the keyword from the filter list.
   - Plan: Implement logic to remove the keyword from the persistent storage.

3. !viewfilters
   - Description: View all active filter keywords.
   - Missing: Implementation logic to retrieve and display the filter keywords.
   - Plan: Implement logic to fetch the keywords from persistent storage and display them.

4. !editfilter
   - Description: Edit an existing filter keyword.
   - Missing: Implementation logic to update the keyword in the filter list.
   - Plan: Implement logic to update the keyword in the persistent storage.

5. !forward
   - Description: Manually forward a message to the appropriate channel.
   - Missing: Implementation logic to forward the message.
   - Plan: Implement logic to fetch the message by ID and forward it to the specified channel.

6. !setzip
   - Description: Set the user's ZIP code.
   - Missing: Implementation logic to store the ZIP code.
   - Plan: Implement logic to store the ZIP code in a persistent storage (e.g., database or in-memory dictionary).

7. !checkzip
   - Description: Check the user's ZIP code.
   - Missing: Implementation logic to retrieve and display the ZIP code.
   - Plan: Implement logic to fetch the ZIP code from persistent storage and display it.

8. !checkstock
   - Description: Check stock and price for a given SKU.
   - Missing: Implementation logic to check stock and price.
   - Plan: Implement logic to fetch stock and price information from an external API or database.

Note: Ensure that all commands have appropriate error handling and logging for better debugging and monitoring.
"""

import discord  # Import the discord module
from discord.ext import commands
import sqlite3
import re
import os
import logging
import time
from config import DISCORD_BOT_TOKEN, CHANNEL_ID, ALLOWED_BOT_IDS  # Import the config module

# Initialize the bot
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

# List of admin user IDs
admin_user_ids = [1234567890, 9876543210, 882914603862994964]  # Replace with actual admin user IDs

def is_admin(ctx):
    return ctx.author.id in admin_user_ids

def setup_commands(bot):
    if not bot.get_command('setvalidationminpercent'):
        @bot.command()
        async def setvalidationminpercent(ctx, percent: int):
            """Set the minimum discount percent."""
            conn = sqlite3.connect('settings.db')
            c = conn.cursor()
            c.execute("UPDATE settings SET value = ? WHERE key = 'min_discount_percent'", (percent,))
            conn.commit()

            # Validate the change by querying the database
            c.execute("SELECT value FROM settings WHERE key = 'min_discount_percent'")
            updated_value = c.fetchone()[0]
            conn.close()

            if updated_value == percent:
                await ctx.send(f"Minimum discount percent set to {percent}%.")
            else:
                await ctx.send(f"Failed to set minimum discount percent to {percent}%.")

    if not bot.get_command('setvalidationmindiscount'):
        @bot.command()
        async def setvalidationmindiscount(ctx, value: float):
            """Set the minimum discount value."""
            conn = sqlite3.connect('settings.db')
            c = conn.cursor()
            c.execute("UPDATE settings SET value = ? WHERE key = 'min_discount_value'", (value,))
            conn.commit()

            # Validate the change by querying the database
            c.execute("SELECT value FROM settings WHERE key = 'min_discount_value'")
            updated_value = c.fetchone()[0]
            conn.close()

            if updated_value == value:
                await ctx.send(f"Minimum discount value set to ${value}.")
            else:
                await ctx.send(f"Failed to set minimum discount value to ${value}.")

    if not bot.get_command('setvalidationmindifference'):
        @bot.command()
        async def setvalidationmindifference(ctx, value: float):
            """Set the minimum discount difference."""
            conn = sqlite3.connect('settings.db')
            c = conn.cursor()
            c.execute("UPDATE settings SET value = ? WHERE key = 'min_discount_difference'", (value,))
            conn.commit()

            # Validate the change by querying the database
            c.execute("SELECT value FROM settings WHERE key = 'min_discount_difference'")
            updated_value = c.fetchone()[0]
            conn.close()

            if updated_value == value:
                await ctx.send(f"Minimum discount difference set to ${value}.")
            else:
                await ctx.send(f"Failed to set minimum discount difference to ${value}.")

    if not bot.get_command('addfilter'):
        @bot.command()
        async def addfilter(ctx, keyword: str):
            """Add a new keyword to the filters."""
            # Implementation needed
            await ctx.send(f"Filter '{keyword}' added. (Not yet implemented)")

    if not bot.get_command('removefilter'):
        @bot.command()
        async def removefilter(ctx, keyword: str):
            """Remove an existing keyword from the filters."""
            # Implementation needed
            await ctx.send(f"Filter '{keyword}' removed. (Not yet implemented)")

    if not bot.get_command('viewfilters'):
        @bot.command()
        async def viewfilters(ctx):
            """View all active filter keywords."""
            # Implementation needed
            await ctx.send("Active filters: (Not yet implemented)")

    if not bot.get_command('editfilter'):
        @bot.command()
        async def editfilter(ctx, old_keyword: str, new_keyword: str):
            """Edit an existing filter keyword."""
            # Implementation needed
            await ctx.send(f"Filter '{old_keyword}' updated to '{new_keyword}'. (Not yet implemented)")

    if not bot.get_command('wrongchannel'):
        @bot.command()
        async def wrongchannel(ctx, channel: str):
            """Alert users that they are posting in the wrong channel."""
            await ctx.send(f"Please post this type of message in the {channel} channel.")

    # Dictionary to store user ZIP codes
    user_zip_codes = {}

    if not bot.get_command('setzip'):
        @bot.command()
        async def setzip(ctx, zip_code: str):
            """Set the user's ZIP code."""
            user_id = ctx.author.id
            user_zip_codes[user_id] = zip_code
            await ctx.send(f"ZIP code set to {zip_code} for user {ctx.author.name}.")

    if not bot.get_command('checkzip'):
        @bot.command()
        async def checkzip(ctx):
            """Check the user's ZIP code."""
            user_id = ctx.author.id
            zip_code = user_zip_codes.get(user_id, "not set")
            await ctx.send(f"Your ZIP code is {zip_code}.")

    if not bot.get_command('checkstock'):
        @bot.command()
        async def checkstock(ctx, sku: str):
            """Check stock and price for a given SKU."""
            # Implementation needed
            await ctx.send(f"Checking stock for SKU {sku}. (Not yet implemented)")

    if not bot.get_command('helpme'):
        @bot.command()
        async def helpme(ctx):
            """List all available command categories."""
            help_message = """
            **Available Command Categories:**

            **Deal Validation Commands:**
            └── `!dealvalidation`

            **Message & Filter Management Commands:**
            └── `!filtermanagement`

            **Channel & Message Forwarding Commands:**
            └── `!channelmanagement`

            **User Personalization Commands:**
            └── `!usermanagement`

            **Store & Price Monitoring Commands:**
            └── `!storemonitoring`

            **General Commands:**
            └── `!general`
            """
            await ctx.send(help_message)

    if not bot.get_command('dealvalidation'):
        @bot.command()
        async def dealvalidation(ctx):
            """List all deal validation commands."""
            conn = sqlite3.connect('settings.db')
            c = conn.cursor()
            c.execute("SELECT key, value FROM settings WHERE key IN ('min_discount_percent', 'min_discount_value', 'min_discount_difference')")
            settings = {row[0]: row[1] for row in c.fetchall()}
            conn.close()

            deal_validation_message = f"""
            **Deal Validation Commands:**

            **Current Settings:**
            ├── Minimum Discount Percent: {settings.get('min_discount_percent', 'Not set')}
            ├── Minimum Discount Value: ${settings.get('min_discount_value', 'Not set')}
            └── Minimum Discount Difference: ${settings.get('min_discount_difference', 'Not set')}

            **Commands:**
            ├── **!setvalidationminpercent <percent>**
            Set the minimum discount percent.

            ├── **!setvalidationmindiscount <value>**
            Set the minimum discount value.

            └── **!setvalidationmindifference <value>**
            Set the minimum discount difference.
            """
            await ctx.send(deal_validation_message)

    if not bot.get_command('filtermanagement'):
        @bot.command()
        async def filtermanagement(ctx):
            """List all filter management commands."""
            filter_management_message = """
            **Message & Filter Management Commands:**

            **Commands:**
            ├── **!addfilter <keyword>**
            Add a new keyword to the filters.

            ├── **!removefilter <keyword>**
            Remove an existing keyword from the filters.

            ├── **!viewfilters**
            View all active filter keywords.

            └── **!editfilter <old_keyword> <new_keyword>**
            Edit an existing filter keyword.
            """
            await ctx.send(filter_management_message)

    if not bot.get_command('channelmanagement'):
        @bot.command()
        async def channelmanagement(ctx):
            """List all channel and message forwarding commands."""
            channel_management_message = """
            **Channel & Message Forwarding Commands:**

            **Commands:**
            ├── **!wrongchannel <channel>**
            Alert users that they are posting in the wrong channel.

            ├── **!forward <message_id>**
            Manually forward a message to the appropriate channel.

            └── **!backlog <minutes>**
            Reprocess messages from the past specified minutes.
            """
            await ctx.send(channel_management_message)

    if not bot.get_command('usermanagement'):
        @bot.command()
        async def usermanagement(ctx):
            """List all user personalization commands."""
            user_management_message = """
            **User Personalization Commands:**

            **Commands:**
            ├── **!setzip <zip_code>**
            Set the user's ZIP code.

            └── **!checkzip**
            Check the user's ZIP code.
            """
            await ctx.send(user_management_message)

    if not bot.get_command('storemonitoring'):
        @bot.command()
        async def storemonitoring(ctx):
            """List all store and price monitoring commands."""
            store_monitoring_message = """
            **Store & Price Monitoring Commands:**

            **Commands:**
            └── **!checkstock <sku>**
            Check stock and price for a given SKU.
            """
            await ctx.send(store_monitoring_message)

    # ...existing code...

if not bot.get_command('helpme'):
    @bot.command()
    async def helpme(ctx):
        """List all available command categories."""
        help_message = """
        **Available Command Categories:**

        **Deal Validation Commands:**
        └── `!dealvalidation`

        **Message & Filter Management Commands:**
        └── `!filtermanagement`

        **Channel & Message Forwarding Commands:**
        └── `!channelmanagement`

        **User Personalization Commands:**
        └── `!usermanagement`

        **Store & Price Monitoring Commands:**
        └── `!storemonitoring`

        **General Commands:**
        └── `!general`
        """

        if is_admin(ctx):
            help_message += """
            **Admin Commands:**
            └── `!admincommands`
            """

        await ctx.send(help_message)

setup_commands(bot)



