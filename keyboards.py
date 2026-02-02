from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# ---------- User ----------
def user_panel():
    kb = InlineKeyboardMarkup()
    kb.add(
        InlineKeyboardButton("🛒 خرید سرویس", callback_data="buy_service"),
        InlineKeyboardButton("🛠 پشتیبانی", callback_data="support")
    )
    return kb

def back_to_user():
    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton("🔙 بازگشت", callback_data="back_user"))
    return kb

def services_kb(services):
    kb = InlineKeyboardMarkup()
    for s in services:
        kb.add(
            InlineKeyboardButton(
                f"🔥 {s[1]} | ⏳ {s[2]} | 💰 {s[3]} تومان",
                callback_data=f"service_{s[0]}"
            )
        )
    kb.add(InlineKeyboardButton("🔙 بازگشت", callback_data="back_user"))
    return kb


# ---------- Admin ----------
def admin_panel():
    kb = InlineKeyboardMarkup()
    kb.add(
        InlineKeyboardButton("🧾 رسیدها", callback_data="admin_receipts"),
        InlineKeyboardButton("🛠 پشتیبانی", callback_data="admin_support")
    )
    return kb

def back_to_admin():
    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton("🔙 بازگشت", callback_data="back_admin"))
    return kb

def receipt_action_kb(rid):
    kb = InlineKeyboardMarkup()
    kb.add(
        InlineKeyboardButton("✅ تایید", callback_data=f"receipt_ok_{rid}"),
        InlineKeyboardButton("❌ رد", callback_data=f"receipt_no_{rid}")
    )
    kb.add(InlineKeyboardButton("🔙 بازگشت", callback_data="back_admin"))
    return kb
