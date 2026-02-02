from keyboards import user_panel
from config import FAKE_SALES_COUNT

def user_welcome(bot, message):
    text = (
        "👋 خوش اومدی\n\n"
        "🚀 وی‌پی‌ان‌های ما ارزان، پرسرعت و پایدار هستند\n\n"
        f"📊 تعداد سرویس‌های خریداری‌شده: +{FAKE_SALES_COUNT}\n\n"
        "👇 از منوی زیر انتخاب کن"
    )
    bot.send_message(message.chat.id, text, reply_markup=user_panel())
