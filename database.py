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


# ---------- Services ----------
def add_service(name, duration, price):
    cursor.execute(
        "INSERT INTO services (name, duration, price) VALUES (?,?,?)",
        (name, duration, price)
    )
    conn.commit()

def get_services():
    cursor.execute("SELECT * FROM services")
    return cursor.fetchall()


# ---------- Receipts ----------
def add_receipt(user_id, photo_id):
    cursor.execute(
        "INSERT INTO receipts (user_id, photo_id, status, date) VALUES (?,?,?,datetime('now'))",
        (user_id, photo_id, "pending")
    )
    conn.commit()

def get_pending_receipts():
    cursor.execute(
        "SELECT id, user_id, photo_id, status, date FROM receipts ORDER BY id DESC"
    )
    return cursor.fetchall()


def update_receipt_status(rid, status):
    cursor.execute(
        "UPDATE receipts SET status=? WHERE id=?",
        (status, rid)
    )
    conn.commit()


# ---------- Support ----------
def add_support(user_id, message):
    cursor.execute(
        "INSERT INTO support (user_id, message, date) VALUES (?,?,datetime('now'))",
        (user_id, message)
    )
    conn.commit()

def get_supports():
    cursor.execute(
        "SELECT id, user_id, message, date FROM support ORDER BY id DESC"
    )
    return cursor.fetchall()

