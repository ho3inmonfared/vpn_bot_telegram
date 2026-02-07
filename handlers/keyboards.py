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
# ------------------------------
# مدیریت سرویس‌ها
# ------------------------------

def admin_services_menu():
    markup = InlineKeyboardMarkup()
    markup.add(
        InlineKeyboardButton("➕ افزودن سرویس", callback_data="service_add"),
        InlineKeyboardButton("✏️ ویرایش سرویس", callback_data="service_edit"),
        InlineKeyboardButton("🗑 حذف سرویس", callback_data="service_delete")
    )
    markup.add(
        InlineKeyboardButton("⬅️ بازگشت", callback_data="admin_menu")
    )
    return markup


def services_list_keyboard(services, prefix):
    markup = InlineKeyboardMarkup()

    for s in services:
        markup.add(
            InlineKeyboardButton(
                f"{s['name']} | {s['price']} تومان",
                callback_data=f"{prefix}_{s['id']}"
            )
        )

    # بازگشت هوشمند
    if prefix == "buy":
        back_callback = "user_menu"
    else:
        back_callback = "admin_services"

    markup.add(
        InlineKeyboardButton("⬅️ بازگشت", callback_data=back_callback)
    )

    return markup


# ==============================
# Receipts / Payments Keyboards
# ==============================

def send_receipt_back_to_menu():
    from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
    markup = InlineKeyboardMarkup()
    markup.add(
        InlineKeyboardButton("⬅️ بازگشت", callback_data="user_menu")
    )
    return markup


def receipt_admin_filter_menu():
    from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
    markup = InlineKeyboardMarkup()
    markup.add(
        InlineKeyboardButton("📥 بررسی‌نشده", callback_data="receipts_pending"),
        InlineKeyboardButton("✅ پاسخ‌داده‌شده", callback_data="receipts_answered")
    )
    markup.add(
        InlineKeyboardButton("⬅️ بازگشت", callback_data="admin_menu")
    )
    return markup


def receipt_admin_action(receipt_id):
    from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

    markup = InlineKeyboardMarkup(row_width=2)

    markup.add(
        InlineKeyboardButton(
            "✉️ پاسخ به کاربر",
            callback_data=f"receipt_reply_{receipt_id}"
        ),
        InlineKeyboardButton(
            "❌ رد رسید",
            callback_data=f"receipt_reject_{receipt_id}"
        )
    )

    markup.add(
        InlineKeyboardButton(
            "⬅️ بازگشت",
            callback_data="receipts_pending"
        )
    )

    return markup

# ==============================
# Support / Tickets Keyboards
# ==============================

def support_user_start_keyboard():
    markup = InlineKeyboardMarkup()
    markup.add(
        InlineKeyboardButton("⬅️ بازگشت", callback_data="user_menu")
    )
    return markup


def support_admin_filter_menu():
    markup = InlineKeyboardMarkup()
    markup.add(
        InlineKeyboardButton("📥 بررسی‌نشده", callback_data="support_pending"),
        InlineKeyboardButton("✅ پاسخ‌داده‌شده", callback_data="support_answered")
    )
    markup.add(
        InlineKeyboardButton("⬅️ بازگشت", callback_data="admin_menu")
    )
    return markup


def support_admin_action(ticket_id):
    markup = InlineKeyboardMarkup(row_width=2)

    markup.add(
        InlineKeyboardButton(
            "✉️ پاسخ به کاربر",
            callback_data=f"support_reply_{ticket_id}"
        ),
        InlineKeyboardButton(
            "❌ رد درخواست",
            callback_data=f"support_reject_{ticket_id}"
        )
    )

    markup.add(
        InlineKeyboardButton(
            "⬅️ بازگشت",
            callback_data="support_pending"
        )
    )

    return markup



