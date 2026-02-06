# ==============================
# Main Entry Point (Phase 1)
# ==============================
from bot_instance import bot


from datetime import datetime

from config import TOKEN, ADMIN_ID
from database import init_db, get_connection
from handlers.keyboards import user_main_menu

import handlers.user
import handlers.admin

# ------------------------------
# Bot Initialization
# ------------------------------



# ------------------------------
# Start Command
# ------------------------------
@bot.message_handler(commands=["start"])
def start_handler(message):
    user_id = message.from_user.id
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT OR IGNORE INTO users (user_id, joined_at) VALUES (?, ?)",
        (user_id, now)
    )
    conn.commit()
    conn.close()

    # تشخیص ادمین یا کاربر
    if user_id == ADMIN_ID:
        text = (
            "👑 <b>پنل مدیریت</b>\n\n"
            "ربات با موفقیت اجرا شد.\n"
            "منتظر دستورات مدیریتی هستیم."
        )

        bot.send_message(message.chat.id, text)

    else:
        from handlers.keyboards import user_main_menu

        text = (
            "🌐 <b>سرویس VPN پرسرعت</b>\n\n"
            "✅ کیفیت بالا\n"
            "💰 قیمت اقتصادی\n"
            "🔥 فروش بالا و رضایت کاربران\n\n"
            "لطفاً یکی از گزینه‌ها را انتخاب کنید:"
        )

        bot.send_message(
            message.chat.id,
            text,
            reply_markup=user_main_menu()
        )



# ------------------------------
# Bot Runner
# ------------------------------
if __name__ == "__main__":
    print("Bot is running...")
    init_db()
    bot.infinity_polling(skip_pending=True)
    
    


