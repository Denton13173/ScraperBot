"""
TODO: Review and Implement Missing Admin Commands

1. !backlog
   - Description: Reprocess messages from the past specified minutes.
   - Missing: Implementation logic to reprocess messages.
   - Plan: Implement logic to fetch messages from the past specified minutes and reprocess them.

2. !viewscheduledtasks
   - Description: Display a list of all scheduled tasks and their next run times.
   - Missing: Implementation logic to retrieve and display scheduled tasks.
   - Plan: Implement logic to fetch scheduled tasks from a task scheduler or database and display them.

3. !clearlogs
   - Description: Clear the log file.
   - Missing: Implementation logic to clear the log file.
   - Plan: Implement logic to delete or truncate the log file.

4. !reloadconfig
   - Description: Reload the bot's configuration from the configuration file.
   - Missing: Implementation logic to reload the configuration.
   - Plan: Implement logic to read the configuration file and update the bot's settings.

5. !restartbot
   - Description: Restart the bot.
   - Missing: Implementation logic to restart the bot.
   - Plan: Implement logic to gracefully shut down and restart the bot.

6. !viewconfig
   - Description: Display the current configuration settings.
   - Missing: Implementation logic to retrieve and display configuration settings.
   - Plan: Implement logic to fetch configuration settings from the configuration file or environment variables and display them.

7. !debugmode
   - Description: Enable or disable debug mode.
   - Missing: Implementation logic to toggle debug mode.
   - Plan: Implement logic to set a debug flag and adjust logging levels accordingly.

8. !viewadmins
   - Description: Display the list of current admin user IDs.
   - Missing: Implementation logic to retrieve and display admin user IDs.
   - Plan: Implement logic to fetch admin user IDs from a persistent storage and display them.

9. !viewcommands
   - Description: Display a list of all non-admin active commands and their descriptions.
   - Missing: Implementation logic to retrieve and display non-admin active commands.
   - Plan: Implement logic to fetch active commands from the bot's command registry and display them.

10. !testcommand
    - Description: Test a specific command to ensure it is working as expected.
    - Missing: Implementation logic to test a command.
    - Plan: Implement logic to execute the specified command and display the result.

11. !botstatus
    - Description: Display the current status of the bot, including uptime, memory usage, and other relevant metrics.
    - Missing: Implementation logic to retrieve and display bot status.
    - Plan: Implement logic to fetch system metrics and display them.

12. !viewdealsettings
    - Description: Display the current settings for deal validation.
    - Missing: Implementation logic to retrieve and display deal validation settings.
    - Plan: Implement logic to fetch deal validation settings from the database and display them.

Note: Ensure that all commands have appropriate error handling and logging for better debugging and monitoring.
"""

import discord  # Import the discord module
import sqlite3  # Import the sqlite3 module
from discord.ext import commands
import os
import logging
import psutil  # Ensure psutil is installed
import time
import sys  # Import the sys module
from config import DISCORD_BOT_TOKEN, CHANNEL_ID, ALLOWED_BOT_IDS  # Import the config module

# Initialize the bot
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

# List of admin user IDs
admin_user_ids = [1234567890, 9876543210, 882914603862994964]  # Replace with actual admin user IDs

# Global variable to track deal validation state
deal_validation_paused = False

def is_admin(ctx):
    return ctx.author.id in admin_user_ids

def setup_admin_commands(bot):
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

    if not bot.get_command('admincommands'):
        @bot.command()
        @commands.check(is_admin)
        async def admincommands(ctx):
            """List all admin commands."""
            admin_commands_message = """
            **Admin Commands:**

            **Commands:**
            ├── **!backlog <minutes>**
            Reprocess messages from the past specified minutes.

            ├── **!viewscheduledtasks**
            Display a list of all scheduled tasks and their next run times.

            ├── **!clearlogs**
            Clear the log file.

            ├── **!reloadconfig**
            Reload the bot's configuration from the configuration file.

            ├── **!restartbot**
            Restart the bot.

            ├── **!viewconfig**
            Display the current configuration settings.

            ├── **!debugmode <on|off>**
            Enable or disable debug mode.

            ├── **!viewadmins**
            Display the list of current admin user IDs.

            ├── **!viewcommands**
            Display a list of all active commands and their descriptions.

            ├── **!testcommand <command>**
            Test a specific command to ensure it is working as expected.

            ├── **!botstatus**
            Display the current status of the bot, including uptime, memory usage, and other relevant metrics.

            └── **!viewdealsettings**
            Display the current settings for deal validation.
            """
            await ctx.send(admin_commands_message)

    if not bot.get_command('backlog'):
        @bot.command()
        @commands.check(is_admin)
        async def backlog(ctx, minutes: int):
            """Reprocess messages from the past specified minutes."""
            now = discord.utils.utcnow()
            past_time = now - discord.utils.timedelta(minutes=minutes)
            async for message in ctx.channel.history(after=past_time):
                await ctx.send(f"Reprocessing message: {message.content}")
                # Add logic to reprocess the message
                # For example, you can call a function to validate and process the message

    if not bot.get_command('pausedealvalidation'):
        @bot.command()
        @commands.check(is_admin)
        async def pausedealvalidation(ctx):
            """Pause the deal validation process."""
            global deal_validation_paused
            deal_validation_paused = True
            await ctx.send("Deal validation has been paused.")

    if not bot.get_command('startdealvalidation'):
        @bot.command()
        @commands.check(is_admin)
        async def startdealvalidation(ctx):
            """Start the deal validation process."""
            global deal_validation_paused
            deal_validation_paused = False
            await ctx.send("Deal validation has been started.")

    if not bot.get_command('viewlogs'):
        @bot.command()
        @commands.check(is_admin)
        async def viewlogs(ctx, lines: int):
            """View the last <lines> lines of the log file."""
            log_file = 'logs/example_log.log'
            if os.path.exists(log_file):
                with open(log_file, 'r') as file:
                    log_lines = file.readlines()[-lines:]
                    await ctx.send(f"```\n{''.join(log_lines)}\n```")
            else:
                await ctx.send("Log file not found.")

    if not bot.get_command('clearlogs'):
        @bot.command()
        @commands.check(is_admin)
        async def clearlogs(ctx):
            """Clear the log file."""
            log_file = 'logs/example_log.log'
            if os.path.exists(log_file):
                open(log_file, 'w').close()
                await ctx.send("Log file cleared.")
            else:
                await ctx.send("Log file not found.")

    if not bot.get_command('reloadconfig'):
        @bot.command()
        @commands.check(is_admin)
        async def reloadconfig(ctx):
            """Reload the bot's configuration from the configuration file."""
            from config import reload as reload_config
            reload_config()
            await ctx.send("Configuration reloaded.")

    if not bot.get_command('restartbot'):
        @bot.command()
        @commands.check(is_admin)
        async def restartbot(ctx):
            """Restart the bot."""
            await ctx.send("Restarting bot...")
            os.execv(sys.executable, ['python'] + sys.argv)

    if not bot.get_command('viewconfig'):
        @bot.command()
        @commands.check(is_admin)
        async def viewconfig(ctx):
            """Display the current configuration settings."""
            config_message = f"""
            **Current Configuration:**
            - DISCORD_BOT_TOKEN: {DISCORD_BOT_TOKEN}
            - CHANNEL_ID: {CHANNEL_ID}
            - ALLOWED_BOT_IDS: {ALLOWED_BOT_IDS}
            """
            await ctx.send(config_message)

    if not bot.get_command('debugmode'):
        @bot.command()
        @commands.check(is_admin)
        async def debugmode(ctx, mode: str):
            """Enable or disable debug mode."""
            if mode.lower() == 'on':
                logging.getLogger().setLevel(logging.DEBUG)
                await ctx.send("Debug mode enabled.")
            elif mode.lower() == 'off':
                logging.getLogger().setLevel(logging.INFO)
                await ctx.send("Debug mode disabled.")
            else:
                await ctx.send("Invalid mode. Use 'on' or 'off'.")

    if not bot.get_command('viewadmins'):
        @bot.command()
        @commands.check(is_admin)
        async def viewadmins(ctx):
            """Display the list of current admin user IDs."""
            await ctx.send(f"Current admins: {', '.join(map(str, admin_user_ids))}")

    if not bot.get_command('viewcommands'):
        @bot.command()
        @commands.check(is_admin)
        async def viewcommands(ctx):
            """Display a list of all active commands and their descriptions."""
            commands_list = [f"**{command.name}**: {command.help}" for command in bot.commands]
            await ctx.send("\n".join(commands_list))

    if not bot.get_command('testcommand'):
        @bot.command()
        @commands.check(is_admin)
        async def testcommand(ctx, command: str):
            """Test a specific command to ensure it is working as expected."""
            await ctx.send(f"Testing command: {command}")
            await ctx.invoke(bot.get_command(command))

    if not bot.get_command('botstatus'):
        @bot.command()
        @commands.check(is_admin)
        async def botstatus(ctx):
            """Display the current status of the bot, including uptime, memory usage, and other relevant metrics."""
            process = psutil.Process(os.getpid())
            uptime = time.time() - process.create_time()
            memory_usage = process.memory_info().rss / 1024 ** 2
            status_message = f"""
            **Bot Status:**
            - Uptime: {uptime:.2f} seconds
            - Memory Usage: {memory_usage:.2f} MB
            """
            await ctx.send(status_message)

    if not bot.get_command('viewdealsettings'):
        @bot.command()
        @commands.check(is_admin)
        async def viewdealsettings(ctx):
            """Display the current settings for deal validation."""
            conn = sqlite3.connect('settings.db')
            c = conn.cursor()
            c.execute("SELECT key, value FROM settings WHERE key IN ('min_discount_percent', 'min_discount_value', 'min_discount_difference')")
            settings = {row[0]: row[1] for row in c.fetchall()}
            conn.close()

            settings_message = f"""
            **Deal Validation Settings:**
            - Minimum Discount Percent: {settings.get('min_discount_percent', 'Not set')}
            - Minimum Discount Value: ${settings.get('min_discount_value', 'Not set')}
            - Minimum Discount Difference: ${settings.get('min_discount_difference', 'Not set')}
            """
            await ctx.send(settings_message)

    if not bot.get_command('viewscheduledtasks'):
        @bot.command()
        @commands.check(is_admin)
        async def viewscheduledtasks(ctx):
            """Display a list of all scheduled tasks and their next run times."""
            # Implementation needed

    # ...existing code...

if not bot.get_command('senddeal'):
    @bot.command()
    @commands.check(is_admin)
    async def senddeal(ctx):
        """Guide the admin in formatting a deal message for validation testing."""
        guide_message = """
        **Deal Message Formatting Guide:**

        To test the deal validation, please format your message as follows:

        `Deal! SKU: <SKU>, Discount: <Discount>%, Price: $<Price>`

        Example:
        `Deal! SKU: 12345, Discount: 20%, Price: $19.99`

        After sending the formatted message, the bot will review and validate it.
        """
        await ctx.send(guide_message)

    if not bot.get_command('explaincommands'):
        @bot.command()
        @commands.check(is_admin)
        async def explaincommands(ctx):
            """Pull a list of all commands and command categories with hyper-detailed explanations."""
            explanations = {
                'setvalidationminpercent': "Set the minimum discount percent. Usage: `!setvalidationminpercent <percent>`",
                'setvalidationmindiscount': "Set the minimum discount value. Usage: `!setvalidationmindiscount <value>`",
                'setvalidationmindifference': "Set the minimum discount difference. Usage: `!setvalidationmindifference <value>`",
                'addfilter': "Add a new keyword to the filters. Usage: `!addfilter <keyword>`",
                'removefilter': "Remove an existing keyword from the filters. Usage: `!removefilter <keyword>`",
                'viewfilters': "View all active filter keywords. Usage: `!viewfilters`",
                'editfilter': "Edit an existing filter keyword. Usage: `!editfilter <old_keyword> <new_keyword>`",
                'wrongchannel': "Alert users that they are posting in the wrong channel. Usage: `!wrongchannel <channel>`",
                'forward': "Manually forward a message to the appropriate channel. Usage: `!forward <message_id>`",
                'backlog': "Reprocess messages from the past specified minutes. Usage: `!backlog <minutes>`",
                'setzip': "Set the user's ZIP code. Usage: `!setzip <zip_code>`",
                'checkzip': "Check the user's ZIP code. Usage: `!checkzip`",
                'checkstock': "Check stock and price for a given SKU. Usage: `!checkstock <sku>`",
                'helpme': "List all available command categories. Usage: `!helpme`",
                'dealvalidation': "List all deal validation commands. Usage: `!dealvalidation`",
                'filtermanagement': "List all filter management commands. Usage: `!filtermanagement`",
                'channelmanagement': "List all channel and message forwarding commands. Usage: `!channelmanagement`",
                'usermanagement': "List all user personalization commands. Usage: `!usermanagement`",
                'storemonitoring': "List all store and price monitoring commands. Usage: `!storemonitoring`",
                'general': "List all general commands. Usage: `!general`",
                'addadmin': "Add a user as an admin. Usage: `!addadmin <USERID>`",
                'removeadmin': "Remove a user from the admin list. Usage: `!removeadmin <USERID>`",
                'pausedealvalidation': "Pause the deal validation process. Usage: `!pausedealvalidation`",
                'startdealvalidation': "Start the deal validation process. Usage: `!startdealvalidation`",
                'viewlogs': "View the last <lines> lines of the log file. Usage: `!viewlogs <lines>`",
                'clearlogs': "Clear the log file. Usage: `!clearlogs`",
                'reloadconfig': "Reload the bot's configuration from the configuration file. Usage: `!reloadconfig`",
                'restartbot': "Restart the bot. Usage: `!restartbot`",
                'viewconfig': "Display the current configuration settings. Usage: `!viewconfig`",
                'debugmode': "Enable or disable debug mode. Usage: `!debugmode <on|off>`",
                'viewadmins': "Display the list of current admin user IDs. Usage: `!viewadmins`",
                'viewcommands': "Display a list of all active commands and their descriptions. Usage: `!viewcommands`",
                'testcommand': "Test a specific command to ensure it is working as expected. Usage: `!testcommand <command>`",
                'botstatus': "Display the current status of the bot, including uptime, memory usage, and other relevant metrics. Usage: `!botstatus`",
                'viewdealsettings': "Display the current settings for deal validation. Usage: `!viewdealsettings`",
                'viewscheduledtasks': "Display a list of all scheduled tasks and their next run times. Usage: `!viewscheduledtasks`"
            }
            explanation_message = "\n".join([f"**{cmd}**: {desc}" for cmd, desc in explanations.items()])
            await ctx.send(explanation_message)

setup_admin_commands(bot)