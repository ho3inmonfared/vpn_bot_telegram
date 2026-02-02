from config import ADMIN_ID
from keyboards import admin_panel

def admin_welcome(bot, message):
    text = (
        "👑 سلام ادمین عزیز\n\n"
        "به پنل مدیریت خوش اومدی 🌟\n"
        "از اینجا می‌تونی همه چیز رو کنترل کنی 🚀"
    )
    bot.send_message(message.chat.id, text, reply_markup=admin_panel())
