import sqlite3

conn = sqlite3.connect("bot.db", check_same_thread=False)
cursor = conn.cursor()

def init_db():
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY,
        username TEXT,
        join_date TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS services (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        duration TEXT,
        price INTEGER
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS receipts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        photo_id TEXT,
        status TEXT,
        date TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS support (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        message TEXT,
        date TEXT
    )
    """)

    conn.commit()
