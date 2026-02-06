# ==============================
# Admin Handlers (Phase 3)
# ==============================

from telebot.types import CallbackQuery
from datetime import datetime

from bot_instance import bot
from config import ADMIN_ID
from database import get_connection
from handlers.keyboards import admin_main_menu

from handlers.keyboards import admin_services_menu, services_list_keyboard

# ------------------------------
# Admin start menu
# ------------------------------
@bot.message_handler(func=lambda m: m.from_user.id == ADMIN_ID, commands=["admin"])
def admin_start(message):
    text = (
        "👑 <b>پنل مدیریت</b>\n\n"
        "لطفاً یکی از گزینه‌های مدیریتی را انتخاب کنید:"
    )

    bot.send_message(
        message.chat.id,
        text,
        reply_markup=admin_main_menu()
    )


# ------------------------------
# Users list
# ------------------------------
@bot.callback_query_handler(func=lambda call: call.data == "admin_users")
def admin_users(call: CallbackQuery):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT user_id, joined_at
        FROM users
        ORDER BY id DESC
        LIMIT 20
    """)
    users = cursor.fetchall()
    conn.close()

    if not users:
        text = "👥 هنوز هیچ کاربری ثبت نشده است."
    else:
        text = "👥 <b>لیست کاربران (آخرین‌ها)</b>\n\n"
        for u in users:
            text += (
                f"🆔 <code>{u['user_id']}</code>\n"
                f"🕒 {u['joined_at']}\n"
                "──────────────\n"
            )

    bot.edit_message_text(
        text,
        call.message.chat.id,
        call.message.message_id,
        reply_markup=admin_main_menu()
    )



@bot.callback_query_handler(func=lambda c: c.data == "admin_services")
def admin_services(call):
    bot.edit_message_text(
        "🛒 <b>مدیریت سرویس‌ها</b>\n\nیکی از گزینه‌ها را انتخاب کنید:",
        call.message.chat.id,
        call.message.message_id,
        reply_markup=admin_services_menu()
    )


# ---------- Add service ----------
@bot.callback_query_handler(func=lambda c: c.data == "service_add")
def service_add(call):
    bot.answer_callback_query(call.id, "➕ افزودن سرویس در فاز بعد تکمیل می‌شود")


# ---------- Edit service ----------
@bot.callback_query_handler(func=lambda c: c.data == "service_edit")
def service_edit(call):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM services")
    services = cursor.fetchall()
    conn.close()

    if not services:
        bot.answer_callback_query(call.id, "❌ سرویسی وجود ندارد")
        return

    bot.edit_message_text(
        "✏️ <b>انتخاب سرویس برای ویرایش</b>",
        call.message.chat.id,
        call.message.message_id,
        reply_markup=services_list_keyboard(services, "edit")
    )


# ---------- Delete service ----------
@bot.callback_query_handler(func=lambda c: c.data == "service_delete")
def service_delete(call):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM services")
    services = cursor.fetchall()
    conn.close()

    if not services:
        bot.answer_callback_query(call.id, "❌ سرویسی وجود ندارد")
        return

    bot.edit_message_text(
        "🗑 <b>انتخاب سرویس برای حذف</b>",
        call.message.chat.id,
        call.message.message_id,
        reply_markup=services_list_keyboard(services, "delete")
    )

# ------------------------------
# Handler عمومی برای back
# ------------------------------
@bot.callback_query_handler(func=lambda c: c.data == "admin_menu")
def admin_back_to_main(call):
    from handlers.keyboards import admin_main_menu
    bot.edit_message_text(
        "👑 <b>پنل مدیریت</b>\n\nلطفاً یکی از گزینه‌های مدیریتی را انتخاب کنید:",
        call.message.chat.id,
        call.message.message_id,
        reply_markup=admin_main_menu()
    )


@bot.callback_query_handler(func=lambda c: c.data == "admin_services")
def admin_back_to_services(call):
    from handlers.keyboards import admin_services_menu
    bot.edit_message_text(
        "🛒 <b>مدیریت سرویس‌ها</b>\n\nیکی از گزینه‌ها را انتخاب کنید:",
        call.message.chat.id,
        call.message.message_id,
        reply_markup=admin_services_menu()
    )
