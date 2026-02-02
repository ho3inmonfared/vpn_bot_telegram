from keyboards import admin_panel, receipt_action_kb, back_to_admin
from database import get_pending_receipts, get_supports

def welcome_admin(bot, message):
    bot.send_message(
        message.chat.id,
        "👑 پنل مدیریت\n\nاز اینجا همه‌چیز دست توئه 😎",
        reply_markup=admin_panel()
    )

def show_receipts(bot, chat_id):
    receipts = get_pending_receipts()
    if not receipts:
        bot.send_message(chat_id, "📭 رسیدی وجود ندارد", reply_markup=back_to_admin())
        return

    for r in receipts:
        rid, user_id, photo_id, status, date = r

        caption = (
            "🧾 رسید پرداخت\n\n"
            f"🆔 کاربر: {user_id}\n"
            f"📅 تاریخ: {date}\n"
            f"📌 وضعیت: {status}"
        )

        if status == "pending":
            bot.send_photo(
                chat_id,
                photo_id,
                caption=caption,
                reply_markup=receipt_action_kb(rid)
            )
        else:
            bot.send_photo(
                chat_id,
                photo_id,
                caption=caption + "\n\n✅ قبلاً بررسی شده",
                reply_markup=back_to_admin()
            )

def show_supports(bot, chat_id):
    supports = get_supports()
    if not supports:
        bot.send_message(chat_id, "📭 پیامی نیست", reply_markup=back_to_admin())
        return

    for s in supports:
        sid, user_id, message, date = s
        bot.send_message(
            chat_id,
            f"""🛠 پشتیبانی

🆔 کاربر: {user_id}
📅 تاریخ: {date}

💬 پیام:
{message}
""",
            reply_markup=back_to_admin()
        )
