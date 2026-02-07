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
from handlers.keyboards import receipt_admin_action
from config import ADMIN_ID



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

@bot.message_handler(commands=["start"])
def start_user(message):
    user_id = message.from_user.id
    if user_id == ADMIN_ID:
        bot.send_message(
            ADMIN_ID,
            "👑 شما ادمین هستید.\n\nبرای ورود به پنل مدیریت از دستور زیر استفاده کنید:\n/admin"
        )
        return
    username = message.from_user.username
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    conn = get_connection()
    cursor = conn.cursor()

    # آیا کاربر قبلاً ثبت شده؟
    cursor.execute(
        "SELECT id FROM users WHERE user_id=?",
        (user_id,)
    )
    exists = cursor.fetchone()

    if not exists:
        # ثبت کاربر جدید
        cursor.execute("""
            INSERT INTO users (user_id, username, joined_at)
            VALUES (?, ?, ?)
        """, (user_id, username, now))
        conn.commit()

        # 🔔 اعلان لحظه‌ای به ادمین
        bot.send_message(
            ADMIN_ID,
            "🟢 <b>کاربر جدید وارد ربات شد</b>\n\n"
            f"🆔 <code>{user_id}</code>\n"
            f"👤 @{username}\n"
            f"🕒 {now}"
        )

    conn.close()

    # ارسال منوی اصلی
    bot.send_message(
        user_id,
        "🌐 <b>سرویس VPN پرسرعت</b>\n\n"
        "✅ کیفیت بالا\n"
        "💰 قیمت اقتصادی\n"
        f"🔥 تعداد فروش: {FAKE_SALES_COUNT}\n\n"
        "لطفاً یکی از گزینه‌ها را انتخاب کنید:",

        reply_markup=user_main_menu()
    )

    set_state(user_id, "MENU")

@bot.message_handler(commands=["buy"])
def buy_command(message):
    if message.from_user.id == ADMIN_ID:
        bot.reply_to(message, "⛔ این دستور فقط برای کاربران است")
        return

    from handlers.keyboards import services_list_keyboard

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM services")
    services = cursor.fetchall()
    conn.close()

    if not services:
        bot.send_message(message.chat.id, "❌ در حال حاضر سرویسی موجود نیست")
        return

    bot.send_message(
        message.chat.id,
        "🛒 <b>انتخاب سرویس</b>\n\nلطفاً یکی از سرویس‌ها را انتخاب کنید:",
        reply_markup=services_list_keyboard(services, "buy")
    )

    set_state(message.from_user.id, "MENU")


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
# Support (User)
# ------------------------------
@bot.callback_query_handler(func=lambda call: call.data == "user_support")
def user_support_start(call: CallbackQuery):
    bot.edit_message_text(
        "🆘 <b>پشتیبانی</b>\n\n"
        "لطفاً پیام خود را بنویسید.\n"
        "📌 فقط پیام متنی قابل ارسال است.",
        call.message.chat.id,
        call.message.message_id,
        reply_markup=back_button("user_menu")
    )

    set_state(call.from_user.id, "WAIT_SUPPORT_MESSAGE")

@bot.message_handler(
    func=lambda m: get_state(m.from_user.id) == "WAIT_SUPPORT_MESSAGE",
    content_types=["text"]
)
def receive_support_message(message):
    if message.text.startswith("/"):
        return

    user_id = message.from_user.id
    text = message.text.strip()
    created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    conn = get_connection()
    cursor = conn.cursor()

    # ✅ اول چک کن تیکت باز دارد یا نه
    cursor.execute("""
        SELECT id FROM support_tickets
        WHERE user_id=? AND status='pending'
    """, (user_id,))
    if cursor.fetchone():
        conn.close()
        bot.send_message(
            user_id,
            "⛔ شما یک درخواست پشتیبانی در حال بررسی دارید.\n\n"
            "🙏 لطفاً تا پاسخ تیم پشتیبانی صبر کنید."
        )
        return

    # ✅ اگر نداشت، ثبت کن
    cursor.execute("""
        INSERT INTO support_tickets (user_id, message, status, created_at)
        VALUES (?, ?, 'pending', ?)
    """, (user_id, text, created_at))

    ticket_id = cursor.lastrowid

    cursor.execute(
        "DELETE FROM user_states WHERE user_id=?",
        (user_id,)
    )

    conn.commit()
    conn.close()

    # پیام به کاربر
    bot.send_message(
        user_id,
        "✅ پیام شما با موفقیت ارسال شد.\n\n"
        "⏳ تیم پشتیبانی در سریع‌ترین زمان ممکن بررسی کرده و پاسخ خواهد داد."
    )


    # ارسال برای ادمین
    from handlers.keyboards import support_admin_action

    bot.send_message(
        ADMIN_ID,
        f"🆘 <b>درخواست پشتیبانی جدید</b>\n\n"
        f"👤 کاربر: <code>{user_id}</code>\n"
        f"🕒 {created_at}\n\n"
        f"💬 پیام:\n{text}",
        reply_markup=support_admin_action(ticket_id)
    )

@bot.message_handler(commands=["support"])
def support_command(message):
    if message.from_user.id == ADMIN_ID:
        bot.reply_to(message, "⛔ این دستور فقط برای کاربران است")
        return

    bot.send_message(
        message.chat.id,
        "🆘 <b>پشتیبانی</b>\n\n"
        "لطفاً پیام خود را بنویسید.\n"
        "📌 فقط پیام متنی قابل ارسال است."
    )

    set_state(message.from_user.id, "WAIT_SUPPORT_MESSAGE")


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

    receipt_id = cursor.lastrowid  # ✅ خیلی مهم

    cursor.execute("DELETE FROM user_states WHERE user_id=?", (user_id,))
    conn.commit()
    conn.close()

    bot.send_photo(
        ADMIN_ID,
        file_id,
        caption=f"📥 رسید جدید\n"
                f"👤 کاربر: {user_id}\n"
                f"🕒 {created_at}",
        reply_markup=receipt_admin_action(receipt_id)
    )


