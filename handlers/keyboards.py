# ==============================
# Keyboards (Phase 2 - User)
# ==============================

from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


def user_main_menu():
    markup = InlineKeyboardMarkup()
    markup.add(
        InlineKeyboardButton("🛒 خرید سرویس", callback_data="user_buy"),
        InlineKeyboardButton("🆘 پشتیبانی", callback_data="user_support")
    )
    return markup


def back_button(to):
    markup = InlineKeyboardMarkup()
    markup.add(
        InlineKeyboardButton("⬅️ بازگشت", callback_data=to)
    )
    return markup

# ==============================
# Admin Keyboards (Phase 3)
# ==============================

def admin_main_menu():
    markup = InlineKeyboardMarkup()
    markup.add(
        InlineKeyboardButton("👥 لیست کاربران", callback_data="admin_users"),
        InlineKeyboardButton("🛒 مدیریت سرویس‌ها", callback_data="admin_services")
    )
    markup.add(
        InlineKeyboardButton("🧾 رسیدهای پرداخت", callback_data="admin_receipts"),
        InlineKeyboardButton("🆘 پشتیبانی", callback_data="admin_support")
    )
    return markup

# ==============================
# Service Management Keyboards
# ==============================

# ------------------------------
# اصلاح دوکمه بازگشت
# ------------------------------
def admin_services_menu():
    from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
    markup = InlineKeyboardMarkup()
    markup.add(
        InlineKeyboardButton("➕ افزودن سرویس", callback_data="service_add"),
        InlineKeyboardButton("✏️ ویرایش سرویس", callback_data="service_edit"),
        InlineKeyboardButton("🗑 حذف سرویس", callback_data="service_delete")
    )
    markup.add(
        InlineKeyboardButton("⬅️ بازگشت", callback_data="admin_menu")  # callback_data دقیق
    )
    return markup


def services_list_keyboard(services, prefix):
    from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
    markup = InlineKeyboardMarkup()
    for s in services:
        markup.add(
            InlineKeyboardButton(
                f"{s['name']} | {s['price']} تومان",
                callback_data=f"{prefix}_{s['id']}"
            )
        )
    markup.add(
        InlineKeyboardButton("⬅️ بازگشت", callback_data="admin_services")  # callback_data درست
    )
    return markup


