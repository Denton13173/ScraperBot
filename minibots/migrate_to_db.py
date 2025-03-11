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
