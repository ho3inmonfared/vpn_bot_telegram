# ==============================
# Database Manager (Phase 1)
# ==============================

import sqlite3
from threading import Lock

DB_NAME = "database.db"
_db_lock = Lock()


def get_connection():
    """
    ایجاد اتصال امن به دیتابیس
    """
    conn = sqlite3.connect(DB_NAME, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """
    ساخت جدول‌های اصلی پروژه
    فقط یک بار در شروع ربات اجرا می‌شود
    """
    with _db_lock:
        conn = get_connection()
        cursor = conn.cursor()

        # ------------------------------
        # جدول کاربران
        # ------------------------------
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER UNIQUE,
            joined_at TEXT
        )
        """)

        # ------------------------------
        # جدول state کاربران
        # ------------------------------
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_states (
            user_id INTEGER PRIMARY KEY,
            state TEXT
        )
        """)
        
        # ------------------------------
        # جدول سرویس‌ها
        # ------------------------------
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS services (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            volume TEXT,
            duration TEXT,
            price INTEGER
        )
        """)


        conn.commit()
        conn.close()
