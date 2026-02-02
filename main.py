import telebot
from config import BOT_TOKEN, ADMIN_ID
from database import init_db, cursor, conn, update_receipt_status
from datetime import datetime

from user import (
    welcome_user, buy_service, select_service,
    handle_photo, start_support, handle_text
)
from admin import welcome_admin, show_receipts, show_supports

bot = telebot.TeleBot(BOT_TOKEN)
init_db()

print("✅ ربات اجرا شد")

@bot.message_handler(commands=["start"])
def start(message):
    cursor.execute("SELECT * FROM users WHERE user_id=?", (message.from_user.id,))
    if not cursor.fetchone():
        cursor.execute(
            "INSERT INTO users VALUES (?,?,?)",
            (message.from_user.id, message.from_user.username, datetime.now().isoformat())
        )
        conn.commit()
        if message.from_user.id != ADMIN_ID:
            bot.send_message(ADMIN_ID, "👤 کاربر جدید عضو شد")

    if message.from_user.id == ADMIN_ID:
        welcome_admin(bot, message)
    else:
        welcome_user(bot, message)


@bot.callback_query_handler(func=lambda call: True)
def callbacks(call):
    bot.answer_callback_query(call.id)

    if call.data == "buy_service":
        buy_service(bot, call)

    elif call.data.startswith("service_"):
        select_service(bot, call)

    elif call.data == "support":
        start_support(bot, call)

    elif call.data == "back_user":
        welcome_user(bot, call.message)

    elif call.data == "back_admin":
        welcome_admin(bot, call.message)

    elif call.data == "admin_receipts":
        show_receipts(bot, call.message.chat.id)

    elif call.data == "admin_support":
        show_supports(bot, call.message.chat.id)

    elif call.data.startswith("receipt_ok_"):
        rid = int(call.data.split("_")[2])
        update_receipt_status(rid, "approved")
        bot.send_message(call.message.chat.id, "✅ رسید تایید شد")

    elif call.data.startswith("receipt_no_"):
        rid = int(call.data.split("_")[2])
        update_receipt_status(rid, "rejected")
        bot.send_message(call.message.chat.id, "❌ رسید رد شد")


@bot.message_handler(content_types=["photo"])
def photo_handler(message):
    handle_photo(bot, message)

@bot.message_handler(func=lambda m: m.text is not None)
def text_handler(message):
    handle_text(bot, message)


bot.infinity_polling()
