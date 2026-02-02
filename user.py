from keyboards import (
    user_panel, services_kb, back_to_user
)
from database import get_services, add_receipt, add_support
from config import CARD_NUMBER, CARD_OWNER, FAKE_SALES_COUNT, ADMIN_ID

user_states = {}

def welcome_user(bot, message):
    bot.send_message(
        message.chat.id,
        f"""👋 خوش اومدی رفیق 😎

🚀 VPN های ما:
⚡ پرسرعت
🛡 پایدار
💰 اقتصادی

📊 تعداد سرویس‌های فعال: +{FAKE_SALES_COUNT}

👇 از منوی زیر انتخاب کن""",
        reply_markup=user_panel()
    )

def buy_service(bot, call):
    services = get_services()
    if not services:
        bot.send_message(
            call.message.chat.id,
            "❌ فعلاً سرویسی برای فروش موجود نیست",
            reply_markup=back_to_user()
        )
        return

    bot.send_message(
        call.message.chat.id,
        "🔥 یکی از سرویس‌های زیر رو انتخاب کن:",
        reply_markup=services_kb(services)
    )

def select_service(bot, call):
    bot.send_message(
        call.message.chat.id,
        f"""💳 مرحله پرداخت

🔢 مبلغ سرویس انتخابی رو به کارت زیر واریز کن:

💳 {CARD_NUMBER}
👤 {CARD_OWNER}

📸 بعد از پرداخت، عکس رسید رو ارسال کن

⏳ بررسی به‌صورت دستی انجام میشه""",
        reply_markup=back_to_user()
    )
    user_states[call.from_user.id] = "WAIT_RECEIPT"

def handle_photo(bot, message):
    if user_states.get(message.from_user.id) == "WAIT_RECEIPT":
        photo_id = message.photo[-1].file_id
        add_receipt(message.from_user.id, photo_id)

        # پیام به کاربر
        bot.send_message(
            message.chat.id,
            "✅ رسیدت ثبت شد\n⏳ لطفاً منتظر تایید ادمین باش",
            reply_markup=back_to_user()
        )

        # اعلان لحظه‌ای به ادمین
        bot.send_photo(
            ADMIN_ID,
            photo_id,
            caption=(
                "🧾 رسید جدید دریافت شد\n\n"
                f"🆔 کاربر: {message.from_user.id}\n"
                f"📅 تاریخ: ارسال شد"
            )
        )

        user_states.pop(message.from_user.id)

def start_support(bot, call):
    bot.send_message(
        call.message.chat.id,
        "🛠 پشتیبانی آنلاین\n\n✍️ پیام خودت رو بنویس، ما در اسرع وقت جواب می‌دیم",
        reply_markup=back_to_user()
    )
    user_states[call.from_user.id] = "SUPPORT"

def handle_text(bot, message):
    if user_states.get(message.from_user.id) == "SUPPORT":
        add_support(message.from_user.id, message.text)

        bot.send_message(
            message.chat.id,
            "✅ پیام شما ثبت شد\n⏳ منتظر پاسخ تیم پشتیبانی باشید",
            reply_markup=back_to_user()
        )

        # اعلان لحظه‌ای به ادمین
        bot.send_message(
            ADMIN_ID,
            f"🛠 پیام پشتیبانی جدید\n\n🆔 {message.from_user.id}\n\n{message.text}"
        )

        user_states.pop(message.from_user.id)
