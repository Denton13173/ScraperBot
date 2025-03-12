import discord

def format_deal_message(deal_info, message):
    """
    Format the deal information into a Discord embed message.

    Parameters:
    deal_info (dict): A dictionary containing the extracted deal information.
    message (discord.Message): The original Discord message containing the deal.

    Returns:
    discord.Embed: The formatted embed message.
    """
    discount = deal_info["discount"]
    price = deal_info["price"]
    original_price = deal_info["original_price"]
    discount_value = original_price - price

    # Format the item title as a hyperlink
    item_title_hyperlink = f"[{deal_info['item_name']}]({deal_info['add_to_cart_link']})"

    # Format the links as hyperlinks
    links_message = "\n".join([f"[{link}]({link})" for link in deal_info["item_links"]]) if deal_info["item_links"] else "No additional links."

    embed = discord.Embed(
        title="New Deal Found!",
        description=f"{item_title_hyperlink}\nSKU: {deal_info['sku']}\nPrice: ${price:.2f}\nOriginal Price: ${original_price:.2f}\nPercentage Off: {discount}%\nDollar Off: ${discount_value:.2f}"
    )
    embed.add_field(name="Add to cart", value=f"[ATC]({deal_info['add_to_cart_link']})", inline=False)
    embed.add_field(name="Links", value=links_message, inline=False)
    embed.add_field(name="Original Message", value=f"[Jump to message](https://discord.com/channels/{message.guild.id}/{message.channel.id}/{message.id})", inline=False)
    if deal_info["image_url"]:
        embed.set_thumbnail(url=deal_info["image_url"])

    return embed