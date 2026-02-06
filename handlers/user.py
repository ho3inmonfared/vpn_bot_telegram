# ==============================
# User Handlers (Phase 2)
# ==============================

from telebot.types import CallbackQuery
from datetime import datetime

from bot_instance import bot
from config import FAKE_SALES_COUNT
from database import get_connection
from handlers.keyboards import user_main_menu, back_button


# ------------------------------
# Helper: set user state
# ------------------------------
def set_state(user_id, state):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT OR REPLACE INTO user_states (user_id, state) VALUES (?, ?)",
        (user_id, state)
    )
    conn.commit()
    conn.close()


def get_state(user_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT state FROM user_states WHERE user_id = ?",
        (user_id,)
    )
    row = cursor.fetchone()
    conn.close()
    return row["state"] if row else None


# ------------------------------
# Start menu (user)
# ------------------------------
@bot.callback_query_handler(func=lambda call: call.data == "user_menu")
def user_menu(call: CallbackQuery):
    text = (
        "🌐 <b>سرویس VPN پرسرعت</b>\n\n"
        "✅ کیفیت بالا\n"
        "💰 قیمت اقتصادی\n"
        f"🔥 تعداد فروش: {FAKE_SALES_COUNT}\n\n"
        "لطفاً یکی از گزینه‌ها را انتخاب کنید:"
    )

    bot.edit_message_text(
        text,
        call.message.chat.id,
        call.message.message_id,
        reply_markup=user_main_menu()
    )
    set_state(call.from_user.id, "MENU")


# ------------------------------
# Buy service (placeholder)
# ------------------------------
@bot.callback_query_handler(func=lambda c: c.data == "user_buy")
def user_buy(call):
    from handlers.keyboards import services_list_keyboard
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM services")
    services = cursor.fetchall()
    conn.close()

    if not services:
        bot.answer_callback_query(call.id, "❌ در حال حاضر سرویسی موجود نیست")
        return

    bot.edit_message_text(
        "🛒 <b>انتخاب سرویس</b>\n\nلطفاً یکی از سرویس‌ها را انتخاب کنید:",
        call.message.chat.id,
        call.message.message_id,
        reply_markup=services_list_keyboard(services, "buy")
    )



# ------------------------------
# Support (locked for next phase)
# ------------------------------
@bot.callback_query_handler(func=lambda call: call.data == "user_support")
def support(call: CallbackQuery):
    bot.answer_callback_query(call.id, "🆘 پشتیبانی در فاز بعدی فعال می‌شود")
    

@bot.callback_query_handler(func=lambda c: c.data == "user_buy")
def user_buy(call):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM services")
    services = cursor.fetchall()
    conn.close()

    if not services:
        bot.answer_callback_query(call.id, "❌ در حال حاضر سرویسی موجود نیست")
        return

    from handlers.keyboards import services_list_keyboard

    bot.edit_message_text(
        "🛒 <b>انتخاب سرویس</b>",
        call.message.chat.id,
        call.message.message_id,
        reply_markup=services_list_keyboard(services, "buy")
    )

