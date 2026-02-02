import telebot
from config import BOT_TOKEN, ADMIN_ID
from database import init_db, cursor, conn
from admin import admin_welcome
from user import user_welcome
from datetime import datetime

bot = telebot.TeleBot(BOT_TOKEN)
init_db()

@bot.message_handler(commands=["start"])
def start(message):
    cursor.execute("SELECT * FROM users WHERE user_id=?", (message.from_user.id,))
    if not cursor.fetchone():
        cursor.execute(
            "INSERT INTO users VALUES (?,?,?)",
            (message.from_user.id, message.from_user.username, datetime.now().isoformat())
        )
        conn.commit()

        if message.from_user.id == ADMIN_ID:
            bot.send_message(ADMIN_ID, "👤 یک کاربر جدید عضو شد")

    if message.from_user.id == ADMIN_ID:
        admin_welcome(bot, message)
    else:
        user_welcome(bot, message)

bot.infinity_polling()
