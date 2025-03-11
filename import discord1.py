import discord
import asyncio
import re
from datetime import datetime, timedelta
from discord.ext import commands, tasks
from urllib.parse import quote_plus

TOKEN = "YOUR_DISCORD_BOT_TOKEN"
SERVER_ID = 1087143160091783208
COMMANDS_CHANNEL_ID = 1346116877843431537

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

# User settings
user_zipcodes = {}  
user_summary_times = {}  
user_preferred_stores = {}  
user_stock_threshold = {}  
user_price_criteria = {}  
user_stock_data = {}  
last_home_depot_prices = {}  

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    summary_task.start()

# Extract stock data from embeds
def extract_stock_data(embed):
    title = embed.title or ""
    description = embed.description or ""
    fields = embed.fields

    sku_match = re.search(r'SKU[:\s]*([\w-]+)', description, re.IGNORECASE)
    sku = sku_match.group(1) if sku_match else "Unknown SKU"

    original_price_match = re.search(r'Online Price\s*\$([\d\.]+)', description)
    original_price = float(original_price_match.group(1)) if original_price_match else None

    discount_match = re.search(r'Lowest Price\s*\$([\d\.]+)', description)
    lowest_found_price = float(discount_match.group(1)) if discount_match else None

    discount_percent = None
    if original_price and lowest_found_price:
        discount_percent = round(((original_price - lowest_found_price) / original_price) * 100)

    stock_results = []
    for field in fields:
        if "Store" in field.name:
            store_info = field.value.split("\n")
            store_id = field.name.split("#")[-1].strip()
            stock, distance, address, price = None, None, None, None

            for line in store_info:
                if "Stock:" in line:
                    stock = int(re.search(r'Stock:\s*(\d+)', line).group(1))
                if "Distance:" in line:
                    distance = float(re.search(r'Distance:\s*([\d\.]+)', line).group(1))
                if "Address:" in line:
                    address = line.replace("Address:", "").strip()
                if "In-Store:" in line:
                    price = float(re.search(r'\$([\d\.]+)', line).group(1))

            stock_results.append((title, store_id, price, stock, address, distance, original_price, discount_percent, sku, datetime.utcnow()))

    return sku, stock_results

@bot.event
async def on_message(message):
    if message.author.bot:
        return
    await bot.process_commands(message)

    if message.embeds:
        for embed in message.embeds:
            sku, stock_results = extract_stock_data(embed)
            if stock_results:
                user_id = message.author.id
                if user_id not in user_stock_data:
                    user_stock_data[user_id] = {}
                if sku not in user_stock_data[user_id]:
                    user_stock_data[user_id][sku] = []
                user_stock_data[user_id][sku].extend(stock_results)

                # Check for new lower Home Depot price
                for entry in stock_results:
                    store_id, price, *_ = entry
                    if "homedepot" in store_id.lower():
                        if sku not in last_home_depot_prices or price < last_home_depot_prices[sku]:
                            last_home_depot_prices[sku] = price
                            await message.channel.send(f"🔔 **New lower price at Home Depot!**\nSKU: {sku} - **${price}**")

@bot.command()
async def setzip(ctx, zipcode: str):
    user_zipcodes[ctx.author.id] = zipcode
    await ctx.send(f"Your ZIP code has been set to {zipcode}.")

@bot.command()
async def setsummarytime(ctx, hours: int):
    user_summary_times[ctx.author.id] = hours
    await ctx.send(f"Your stock summary will now be sent every {hours} hours.")

@bot.command()
async def setstores(ctx, *stores):
    user_preferred_stores[ctx.author.id] = list(stores)
    await ctx.send(f"Monitoring only: {', '.join(stores)}")

@bot.command()
async def setstockthreshold(ctx, min_stock: int):
    user_stock_threshold[ctx.author.id] = min_stock
    await ctx.send(f"You will only receive alerts for stock above {min_stock}.")

@bot.command()
async def setpricecriteria(ctx, price: float, discount: int):
    user_price_criteria[ctx.author.id] = (price, discount)
    await ctx.send(f"Alerts set for items over **${price}** with at least **{discount}% off**.")

@bot.command()
async def clearstock(ctx):
    user_stock_data[ctx.author.id] = {}
    await ctx.send("Your stock data has been cleared.")

@bot.command()
async def helpme(ctx):
    settings = f"""
**Your Current Settings**
ZIP Code: {user_zipcodes.get(ctx.author.id, 'Not set')}
Summary Interval: {user_summary_times.get(ctx.author.id, '24 hours')}
Preferred Stores: {', '.join(user_preferred_stores.get(ctx.author.id, ['All']))}
Stock Threshold: {user_stock_threshold.get(ctx.author.id, 1)}
Price Criteria: {user_price_criteria.get(ctx.author.id, (100, 75))}
"""
    commands = """
**Available Commands**
!setzip <ZIP> - Set your ZIP code
!setsummarytime <hours> - Set stock summary time
!setstores <store1> <store2> ... - Select stores to monitor
!setstockthreshold <min_stock> - Minimum stock required for alerts
!setpricecriteria <price> <discount> - Set base price & discount % for alerts
!clearstock - Reset stored stock data
!helpme - Show all commands & current settings
"""
    await ctx.send(f"```{settings}\n{commands}```")

async def send_stock_summary(user):
    user_id = user.id
    if user_id not in user_stock_data or not user_stock_data[user_id]:
        await user.send("No stock check results in the past 24 hours.")
        return

    summary = "**Stock Check Summary - Last 24 Hours**\n\n"
    now = datetime.utcnow()
    valid_entries = {sku: [entry for entry in stock_data if (now - entry[-1]) <= timedelta(hours=24)]
                     for sku, stock_data in user_stock_data[user_id].items()}

    for sku, stock_entries in valid_entries.items():
        stock_entries.sort(key=lambda x: x[2])  # Sort by lowest price

        lowest_price = stock_entries[0][2]
        item_title = stock_entries[0][0]

        summary += f"**{item_title}** {sku}\nLowest Found Price: ${lowest_price}\n\n"

        for entry in stock_entries:
            store_id, price, stock, address, timestamp = entry[1], entry[2], entry[3], entry[4], entry[-1]
            google_maps_link = f"https://www.google.com/maps/search/?api=1&query={quote_plus(address)}"
            summary += f"[Home Depot #{store_id} - {address}]({google_maps_link})\n"
            summary += f"Stock: {stock}\nPrice: ${price} 🔥\nLast Checked: {timestamp.strftime('%Y-%m-%d %H:%M:%S UTC')}\n\n"

    await user.send(summary)

@tasks.loop(hours=24)
async def summary_task():
    for user_id in user_stock_data.keys():
        user = bot.get_user(user_id)
        if user:
            await send_stock_summary(user)

bot.run(TOKEN)
