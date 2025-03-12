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
