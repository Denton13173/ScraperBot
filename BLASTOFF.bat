@echo off
REM Change to the directory where the bot script is located
cd c:\Users\coryd\ScraperBot

REM Activate the virtual environment
call bot_env\Scripts\activate

REM Run the bot script
python import_discord.py

REM Keep the command prompt open
pause