## Phase 10: Mini-Bots and Automation Scripts

To streamline the development process, the following mini-bots and scripts are recommended. These will help automate repetitive tasks, ensure consistency, and make the development process more efficient.

1. **Environment Setup Script**
   - Automates the installation of Python, Git, and VS Code extensions.
   - Sets up the virtual environment and installs required libraries.

**How to Do It:**
1. Create a script named `setup_environment.cmd`:
   ```cmd
   @echo off
   :: Install Python
   echo Installing Python...
   :: Add Python installation commands here

   :: Install Git
   echo Installing Git...
   :: Add Git installation commands here

   :: Install VS Code extensions
   echo Installing VS Code extensions...
   code --install-extension ms-python.python
   code --install-extension github.copilot

   :: Set up virtual environment
   echo Setting up virtual environment...
   python -m venv bot_env
   bot_env\Scripts\activate
   pip install discord.py python-dotenv pyautogui

   echo Environment setup complete.
   pause
   ```

2. **Git Auto-Push Scheduler**
   - Automates the scheduling of the `git_auto_push.bat` script using Task Scheduler on Windows.

**How to Do It:**
1. Create a script named `schedule_git_auto_push.cmd`:
   ```cmd
   @echo off
   echo Scheduling Git auto-push script...
   schtasks /create /tn "GitAutoPush" /tr "C:\Users\coryd\ScraperBot\git_auto_push.bat" /sc minute /mo 5 /f
   echo Git auto-push script scheduled.
   pause
   ```

3. **Discord Bot Token Manager**
   - Securely manages and updates the `DISCORD_BOT_TOKEN` in the `.env` file.

**How to Do It:**
1. Create a script named `manage_token.py`:
   ```python
   import os

   def update_token():
       token = input("Enter your Discord Bot Token: ")
       with open('.env', 'w') as env_file:
           env_file.write(f"DISCORD_BOT_TOKEN={token}\n")
       print("Token updated successfully.")

   if __name__ == "__main__":
       update_token()
   ```

4. **Message Parsing Tester**
   - Simulates sending messages to the Discord bot for testing message parsing and deal extraction.

**How to Do It:**
1. Create a script named `message_tester.py`:
   ```python
   import discord
   import asyncio

   async def send_test_message(bot, channel_id, content):
       channel = bot.get_channel(channel_id)
       await channel.send(content)

   if __name__ == "__main__":
       bot = discord.Client()
       bot.run('YOUR_DISCORD_BOT_TOKEN')
       asyncio.run(send_test_message(bot, YOUR_CHANNEL_ID, "Test deal message with SKU and discount"))
   ```

5. **Deal Validation Script**
   - Validates the extracted deals by checking if they meet certain criteria (e.g., discount range, valid SKU format).

**How to Do It:**
1. Create a script named `validate_deals.py`:
   ```python
   def validate_deal(deal):
       if not (0 <= deal['discount'] <= 100):
           return False
       if not deal['sku'].isdigit():
           return False
       return True

   if __name__ == "__main__":
       test_deal = {'sku': '12345', 'discount': 50}
       print(validate_deal(test_deal))
   ```

6. **Database Migration Script**
   - Migrates in-memory data structures to a database.

**How to Do It:**
1. Create a script named `migrate_to_db.py`:
   ```python
   import sqlite3

   def migrate_data(deals):
       conn = sqlite3.connect('deals.db')
       c = conn.cursor()
       c.execute('''CREATE TABLE IF NOT EXISTS deals (sku TEXT, discount INTEGER)''')
       for deal in deals:
           c.execute("INSERT INTO deals (sku, discount) VALUES (?, ?)", (deal['sku'], deal['discount']))
       conn.commit()
       conn.close()

   if __name__ == "__main__":
       sample_deals = [{'sku': '12345', 'discount': 50}, {'sku': '67890', 'discount': 30}]
       migrate_data(sample_deals)
   ```

7. **User Command Tester**
   - Simulates user commands (e.g., `!setzip`, `!checkzip`) and verifies the bot's responses.

**How to Do It:**
1. Create a script named `command_tester.py`:
   ```python
   import discord
   import asyncio

   async def send_command(bot, channel_id, command):
       channel = bot.get_channel(channel_id)
       await channel.send(command)

   if __name__ == "__main__":
       bot = discord.Client()
       bot.run('YOUR_DISCORD_BOT_TOKEN')
       asyncio.run(send_command(bot, YOUR_CHANNEL_ID, "!setzip 12345"))
   ```

8. **Channel Creation Validator**
   - Checks if the designated "Deals" channel exists and creates it if it doesn't.

**How to Do It:**
1. Create a script named `validate_channel.py`:
   ```python
   import discord
   import asyncio

   async def validate_channel(bot, guild_id, channel_name):
       guild = bot.get_guild(guild_id)
       channel = discord.utils.get(guild.channels, name=channel_name)
       if not channel:
           await guild.create_text_channel(channel_name)
           print(f"Channel '{channel_name}' created.")
       else:
           print(f"Channel '{channel_name}' already exists.")

   if __name__ == "__main__":
       bot = discord.Client()
       bot.run('YOUR_DISCORD_BOT_TOKEN')
       asyncio.run(validate_channel(bot, YOUR_GUILD_ID, "deals"))
   ```

9. **AI Model Trainer**
   - Trains and updates the machine learning model used for deal prioritization.

**How to Do It:**
1. Create a script named `train_model.py`:
   ```python
   from sklearn.model_selection import train_test_split
   from sklearn.ensemble import RandomForestClassifier
   import joblib

   def train_model(data):
       X = data[['sku', 'discount']]
       y = data['priority']
       X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
       model = RandomForestClassifier()
       model.fit(X_train, y_train)
       joblib.dump(model, 'deal_priority_model.pkl')
       print("Model trained and saved.")

   if __name__ == "__main__":
       sample_data = [{'sku': '12345', 'discount': 50, 'priority': 1}, {'sku': '67890', 'discount': 30, 'priority': 0}]
       train_model(sample_data)
   ```

10. **Deployment Script**
    - Automates the deployment of the bot to cloud platforms like Heroku or AWS.

**How to Do It:**
1. Create a script named `deploy_bot.sh`:
   ```bash
   #!/bin/bash
   echo "Deploying bot to Heroku..."
   heroku create
   git push heroku main
   heroku config:set DISCORD_BOT_TOKEN=YOUR_DISCORD_BOT_TOKEN
   echo "Bot deployed successfully."
   ```

11. **Logging and Monitoring Setup**
    - Sets up logging and monitoring for the bot.

**How to Do It:**
1. Create a script named `setup_logging.py`:
   ```python
   import logging

   def setup_logging():
       logging.basicConfig(filename='bot.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
       logging.info("Logging setup complete.")

   if __name__ == "__main__":
       setup_logging()
   ```

12. **Documentation Generator**
    - Generates and updates documentation (e.g., README.md, Changelog.md) based on the current state of the project.

**How to Do It:**
1. Create a script named `generate_docs.py`:
   ```python
   def generate_readme():
       with open('README.md', 'w') as readme:
           readme.write("# ScraperBot\n\n")
           readme.write("## Setup Instructions\n")
           readme.write("1. Install Python, Git, and VS Code.\n")
           readme.write("2. Set up the virtual environment and install dependencies.\n")
           readme.write("3. Configure the `.env` file with your Discord bot token.\n")
           readme.write("4. Run the bot using `python import_discord1.py`.\n")
           readme.write("\n## Features\n")
           readme.write("- Message parsing and deal extraction.\n")
           readme.write("- User interactivity and command handling.\n")
           readme.write("- Automated forwarding and category management.\n")
           readme.write("- Advanced AI features for deal prioritization.\n")

   def generate_changelog():
       with open('Changelog.md', 'w') as changelog:
           changelog.write("# Changelog\n\n")
           changelog.write("## [Unreleased]\n")
           changelog.write("- Initial release.\n")

   if __name__ == "__main__":
       generate_readme()
       generate_changelog()
   ```

These mini-bots and scripts will help automate various aspects of the development process, making it easier to manage and maintain the ScraperBot project.