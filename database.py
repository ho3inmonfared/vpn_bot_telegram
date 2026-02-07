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

        # --- migration: username ---
        cursor.execute("PRAGMA table_info(users)")
        columns = [c[1] for c in cursor.fetchall()]

        if "username" not in columns:
            cursor.execute(
                "ALTER TABLE users ADD COLUMN username TEXT"
            )


        cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_states (
            user_id INTEGER PRIMARY KEY,
            state TEXT,
            data TEXT
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
        
        # ------------------------------
        # جدول رسیدهای پرداخت
        # ------------------------------
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS receipts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            service_id INTEGER,
            photo_id TEXT,
            status TEXT DEFAULT 'pending', -- pending / approved / rejected
            created_at TEXT
        )
        """)
        
            # --- migration: admin_response ---
        cursor.execute("PRAGMA table_info(receipts)")
        columns = [c[1] for c in cursor.fetchall()]

        if "admin_response" not in columns:
            cursor.execute(
                "ALTER TABLE receipts ADD COLUMN admin_response TEXT"
            )

        if "responded_at" not in columns:
            cursor.execute(
                "ALTER TABLE receipts ADD COLUMN responded_at TEXT"
            )

        # ------------------------------
        # جدول پشتیبانی (Support Tickets)
        # ------------------------------
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS support_tickets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            message TEXT,
            status TEXT DEFAULT 'pending', -- pending / answered / rejected
            admin_response TEXT,
            created_at TEXT,
            responded_at TEXT
        )
        """)
        
        conn.commit()
        conn.close()
