#!/bin/bash
echo "Deploying bot to Heroku..."
heroku create
git push heroku main
heroku config:set DISCORD_BOT_TOKEN=YOUR_DISCORD_BOT_TOKEN
echo "Bot deployed successfully."
