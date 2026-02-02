import telebot
from config import BOT_TOKEN, ADMIN_ID
from database import init_db, cursor, conn
from admin import admin_welcome
from user import user_welcome
from datetime import datetime
import sys

try:
    bot = telebot.TeleBot(BOT_TOKEN)
    init_db()
    print("✅ ربات با موفقیت اجرا شد و به تلگرام وصل شد")

except Exception as e:
    print("❌ خطا در اجرای ربات:")
    print(e)
    sys.exit(1)


@bot.message_handler(commands=["start"])
def start(message):
    try:
        cursor.execute("SELECT * FROM users WHERE user_id=?", (message.from_user.id,))
        user_exists = cursor.fetchone()

        if not user_exists:
            cursor.execute(
                "INSERT INTO users VALUES (?,?,?)",
                (
                    message.from_user.id,
                    message.from_user.username,
                    datetime.now().isoformat()
                )
            )
            conn.commit()

            # اطلاع به ادمین فقط وقتی کاربر جدید واقعاً کاربره
            if message.from_user.id != ADMIN_ID:
                bot.send_message(
                    ADMIN_ID,
                    f"👤 کاربر جدید عضو شد\n\n"
                    f"🆔 {message.from_user.id}\n"
                    f"👤 @{message.from_user.username}"
                )

        # تشخیص نقش
        if message.from_user.id == ADMIN_ID:
            admin_welcome(bot, message)
        else:
            user_welcome(bot, message)

    except Exception as e:
        print("❌ خطا در هندل /start")
        print(e)


print("🤖 ربات در حال polling است...")
bot.infinity_polling()
