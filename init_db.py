import sqlite3

def init_db():
    conn = sqlite3.connect('settings.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS settings (key TEXT PRIMARY KEY, value REAL)''')
    c.execute("INSERT OR IGNORE INTO settings (key, value) VALUES ('min_discount_percent', 50)")
    c.execute("INSERT OR IGNORE INTO settings (key, value) VALUES ('min_discount_value', 20)")
    c.execute("INSERT OR IGNORE INTO settings (key, value) VALUES ('min_discount_difference', 1)")
    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()