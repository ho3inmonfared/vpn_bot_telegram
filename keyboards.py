from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

def admin_panel():
    kb = InlineKeyboardMarkup()
    kb.add(
        InlineKeyboardButton("👥 لیست کاربران", callback_data="admin_users"),
        InlineKeyboardButton("🧾 رسیدها", callback_data="admin_receipts"),
    )
    kb.add(
        InlineKeyboardButton("🛠 پشتیبانی", callback_data="admin_support"),
        InlineKeyboardButton("📦 مدیریت سرویس‌ها", callback_data="admin_services")
    )
    return kb

def user_panel():
    kb = InlineKeyboardMarkup()
    kb.add(
        InlineKeyboardButton("🛒 خرید سرویس", callback_data="buy_service"),
        InlineKeyboardButton("🛠 پشتیبانی", callback_data="support")
    )
    return kb
