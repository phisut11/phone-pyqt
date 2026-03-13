import sqlite3

db = sqlite3.connect("phone.db")
cursor = db.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS phone(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    brand TEXT,
    model TEXT,
    price INTEGER,
    ram INTEGER,
    storage INTEGER
)
""")

db.commit()