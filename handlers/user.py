# ==============================
# User Handlers (Phase 2)
# ==============================

from telebot.types import CallbackQuery
from datetime import datetime

from bot_instance import bot
from config import FAKE_SALES_COUNT
from database import get_connection
from handlers.keyboards import user_main_menu, back_button
from handlers.keyboards import send_receipt_back_to_menu


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

from config import ADMIN_ID

@bot.callback_query_handler(func=lambda c: c.data == "user_menu_back")
def user_menu_back(call):
    if call.from_user.id == ADMIN_ID:
        bot.answer_callback_query(call.id, "⛔ این دکمه فقط برای کاربران است")
        return

    bot.edit_message_text(
        "🌐 <b>سرویس VPN پرسرعت</b>\n\nلطفاً یکی از گزینه‌ها را انتخاب کنید:",
        call.message.chat.id,
        call.message.message_id,
        reply_markup=user_main_menu()
    )

# -------------------------------
# Callback خرید سرویس – نمایش لیست
# -------------------------------
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

# ------------------------------
# مرحله ارسال رسید (callback خرید سرویس)
# ------------------------------
@bot.callback_query_handler(func=lambda c: c.data.startswith("buy_"))
def select_service(call):
    service_id = int(call.data.split("_")[1])
    user_id = call.from_user.id

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM receipts WHERE user_id=? AND status='pending'", (user_id,))
    existing = cursor.fetchone()
    conn.close()

    if existing:
        bot.answer_callback_query(call.id, "⛔ شما یک رسید در انتظار دارید")
        return

    # ذخیره موقت سرویس انتخابی در state ساده
    cursor = get_connection().cursor()
    cursor.execute(
        "INSERT OR REPLACE INTO user_states (user_id, state, data) VALUES (?, ?, ?)",
        (user_id, "WAIT_RECEIPT", str(service_id))
    )
    cursor.connection.commit()
    cursor.connection.close()

    # پیام مبلغ و کارت
    from config import CARD_NUMBER, CARD_NAME
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM services WHERE id=?", (service_id,))
    service = cursor.fetchone()
    conn.close()

    bot.edit_message_text(
        f"💳 مبلغ: {service['price']} تومان\n"
        f"شماره کارت: {CARD_NUMBER}\n"
        f"نام صاحب کارت: {CARD_NAME}\n\n"
        "📸 لطفاً رسید پرداخت را به صورت عکس ارسال کنید",
        call.message.chat.id,
        call.message.message_id,
        reply_markup=send_receipt_back_to_menu()
    )

@bot.message_handler(content_types=["photo"])
def receive_photo(message):
    user_id = message.from_user.id

    # بررسی state
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT state, data FROM user_states WHERE user_id=?", (user_id,))
    row = cursor.fetchone()
    if not row or row["state"] != "WAIT_RECEIPT":
        bot.reply_to(message, "⛔ شما در حال ارسال رسید نیستید")
        conn.close()
        return

    service_id = int(row["data"])
    file_id = message.photo[-1].file_id
    created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # ذخیره رسید
    cursor.execute(
        "INSERT INTO receipts (user_id, service_id, photo_id, created_at) VALUES (?, ?, ?, ?)",
        (user_id, service_id, file_id, created_at)
    )
    # پاک کردن state
    cursor.execute("DELETE FROM user_states WHERE user_id=?", (user_id,))
    conn.commit()
    conn.close()

    bot.reply_to(message, "✅ رسید شما دریافت شد و در حال بررسی است")
    
    # اطلاع ادمین
    from config import ADMIN_ID
    bot.send_message(ADMIN_ID, f"📥 رسید جدید از کاربر {user_id} دریافت شد")
