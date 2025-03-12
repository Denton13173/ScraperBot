import re

def extract_deal_info(embed):
    """
    Extract SKU, discount, price, and links from the embed.

    Parameters:
    embed (discord.Embed): The embed object containing the deal information.

    Returns:
    dict: A dictionary containing the extracted information.
    """
    sku = None
    discount = None
    price = None
    add_to_cart_link = None
    item_links = []
    item_name = embed.title if embed.title else "Unknown Item"
    site = embed.author.name if embed.author else "Unknown Site"
    image_url = embed.thumbnail.url if embed.thumbnail else None

    for field in embed.fields:
        if "sku" in field.name.lower():
            sku = field.value
        elif "percentage off" in field.name.lower():
            discount = float(field.value.strip('%'))
        elif "price" in field.name.lower() and "original" not in field.name.lower():
            price = float(field.value.strip('$'))
        elif "add to cart" in field.name.lower():
            add_to_cart_link = field.value

    # Extract item links from the description
    if embed.description:
        item_links = re.findall(r'(https?://\S+)', embed.description)

    return {
        "sku": sku,
        "discount": discount,
        "price": price,
        "add_to_cart_link": add_to_cart_link,
        "item_links": item_links,
        "item_name": item_name,
        "site": site,
        "image_url": image_url
    }

def extract_deal_info_from_text(content):
    """
    Extract SKU, discount, and price from the plain text content.

    Parameters:
    content (str): The plain text content containing the deal information.

    Returns:
    dict: A dictionary containing the extracted information.
    """
    sku_match = re.search(r"SKU\s*:\s*(\S+)", content, re.IGNORECASE)
    discount_match = re.search(r"percentage off\s*:\s*(\d+)%", content, re.IGNORECASE)
    price_match = re.search(r"price\s*:\s*\$?(\d+(\.\d{2})?)", content, re.IGNORECASE)
    add_to_cart_match = re.search(r"add to cart\s*:\s*(\S+)", content, re.IGNORECASE)
    item_links = re.findall(r'(https?://\S+)', content)
    item_name = re.search(r"New Item\s*(.*)", content, re.IGNORECASE).group(1) if re.search(r"New Item\s*(.*)", content, re.IGNORECASE) else "Unknown Item"
    site = "Unknown Site"

    return {
        "sku": sku_match.group(1) if sku_match else None,
        "discount": float(discount_match.group(1)) if discount_match else None,
        "price": float(price_match.group(1)) if price_match else None,
        "add_to_cart_link": add_to_cart_match.group(1) if add_to_cart_match else None,
        "item_links": item_links,
        "item_name": item_name,
        "site": site
    }