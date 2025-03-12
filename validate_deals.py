import sqlite3

def get_settings():
    conn = sqlite3.connect('settings.db')
    c = conn.cursor()
    c.execute("SELECT key, value FROM settings")
    settings = {row[0]: float(row[1]) if row[1] is not None else None for row in c.fetchall()}
    conn.close()
    return settings

def validate_deal(deal):
    """
    Validate the deal data.

    Parameters:
    deal (dict): A dictionary containing 'discount', 'price', and 'original_price' keys.

    Returns:
    bool: True if the deal is valid, False otherwise.
    """
    settings = get_settings()
    min_discount_percent = settings.get('min_discount_percent', 50)
    min_discount_value = settings.get('min_discount_value', 20)
    min_discount_difference = settings.get('min_discount_difference', 1)

    discount_percent = deal['discount']
    discount_value = deal['original_price'] - deal['price']
    discount_difference = deal['original_price'] - deal['price']

    # Validate each criterion independently
    if min_discount_percent is not None and discount_percent < min_discount_percent:
        return False
    if min_discount_value is not None and discount_value < min_discount_value:
        return False
    if min_discount_difference is not None and discount_difference < min_discount_difference:
        return False

    return True

if __name__ == "__main__":
    # Test the validate_deal function with a sample deal
    test_deal = {'discount': 50, 'price': 50, 'original_price': 100}
    print(validate_deal(test_deal))  # Expected output: True