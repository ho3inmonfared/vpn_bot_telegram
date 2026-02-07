# ==============================
# Admin Handlers (Phase 3 + Fix message is not modified)
# ==============================

from telebot.types import CallbackQuery
from datetime import datetime

from bot_instance import bot
from config import ADMIN_ID
from database import get_connection
from handlers.keyboards import admin_main_menu

from handlers.keyboards import admin_services_menu, services_list_keyboard
from handlers.keyboards import receipt_admin_filter_menu, receipt_admin_action
from handlers.keyboards import (
    support_admin_filter_menu,
    support_admin_action
)



# ------------------------------
# Admin start menu
# ------------------------------
@bot.message_handler(func=lambda m: m.from_user.id == ADMIN_ID, commands=["admin"])
def admin_start(message):
    text = (
        "👑 <b>پنل مدیریت</b>\n\n"
        "لطفاً یکی از گزینه‌های مدیریتی را انتخاب کنید:"
    )

    bot.send_message(
        message.chat.id,
        text,
        reply_markup=admin_main_menu()
    )


# ------------------------------
# Users list
# ------------------------------
@bot.callback_query_handler(func=lambda call: call.data == "admin_users")
def admin_users(call: CallbackQuery):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT user_id, joined_at
        FROM users
        ORDER BY id DESC
        LIMIT 20
    """)
    users = cursor.fetchall()
    conn.close()

    if not users:
        text = "👥 هنوز هیچ کاربری ثبت نشده است."
    else:
        text = "👥 <b>لیست کاربران (آخرین‌ها)</b>\n\n"
        for u in users:
            text += (
                f"🆔 <code>{u['user_id']}</code>\n"
                f"🕒 {u['joined_at']}\n"
                "──────────────\n"
            )

    # fix message is not modified
    bot.send_message(
        call.message.chat.id,
        text,
        reply_markup=admin_main_menu()
    )


# ------------------------------
# Admin Services Menu
# ------------------------------
@bot.callback_query_handler(func=lambda c: c.data == "admin_services")
def admin_services(call):
    # fix message is not modified
    bot.send_message(
        call.message.chat.id,
        "🛒 <b>مدیریت سرویس‌ها</b>\n\nیکی از گزینه‌ها را انتخاب کنید:",
        reply_markup=admin_services_menu()
    )


# ---------- افزودن سرویس ----------
@bot.callback_query_handler(func=lambda c: c.data == "service_add")
def service_add(call):
    msg = bot.send_message(call.message.chat.id, "نام سرویس را وارد کنید:")
    bot.register_next_step_handler(msg, process_service_name)


def process_service_name(message):
    name = message.text
    msg = bot.send_message(message.chat.id, "حجم سرویس را وارد کنید (مثلاً 5GB):")
    bot.register_next_step_handler(msg, process_service_volume, name)


def process_service_volume(message, name):
    volume = message.text
    msg = bot.send_message(message.chat.id, "مدت سرویس را وارد کنید (مثلاً 30 روز):")
    bot.register_next_step_handler(msg, process_service_duration, name, volume)


def process_service_duration(message, name, volume):
    duration = message.text
    msg = bot.send_message(message.chat.id, "قیمت سرویس را وارد کنید (تومان):")
    bot.register_next_step_handler(msg, process_service_price, name, volume, duration)


def process_service_price(message, name, volume, duration):
    try:
        price = int(message.text)
    except:
        msg = bot.send_message(message.chat.id, "❌ قیمت باید عدد باشد، دوباره وارد کنید:")
        bot.register_next_step_handler(msg, process_service_price, name, volume, duration)
        return

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO services (name, volume, duration, price) VALUES (?, ?, ?, ?)",
        (name, volume, duration, price)
    )
    conn.commit()
    conn.close()

    bot.send_message(message.chat.id, f"✅ سرویس {name} با موفقیت اضافه شد")

    # fix message is not modified: use send_message
    bot.send_message(
        message.chat.id,
        "🛒 <b>مدیریت سرویس‌ها</b>\n\nیکی از گزینه‌ها را انتخاب کنید:",
        reply_markup=admin_services_menu()
    )


# ---------- Edit service ----------
@bot.callback_query_handler(func=lambda c: c.data == "service_edit")
def service_edit(call):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM services")
    services = cursor.fetchall()
    conn.close()

    if not services:
        bot.answer_callback_query(call.id, "❌ سرویسی وجود ندارد")
        return

    bot.send_message(
        call.message.chat.id,
        "✏️ <b>انتخاب سرویس برای ویرایش</b>",
        reply_markup=services_list_keyboard(services, "edit")
    )


@bot.callback_query_handler(func=lambda c: c.data.startswith("edit_"))
def edit_service_select(call):
    service_id = int(call.data.split("_")[1])
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM services WHERE id=?", (service_id,))
    service = cursor.fetchone()
    conn.close()

    msg = bot.send_message(call.message.chat.id, f"نام سرویس ({service['name']}) را وارد کنید:")
    bot.register_next_step_handler(msg, edit_service_name, service_id)


def edit_service_name(message, service_id):
    name = message.text
    msg = bot.send_message(message.chat.id, "حجم سرویس را وارد کنید:")
    bot.register_next_step_handler(msg, edit_service_volume, service_id, name)


def edit_service_volume(message, service_id, name):
    volume = message.text
    msg = bot.send_message(message.chat.id, "مدت سرویس را وارد کنید:")
    bot.register_next_step_handler(msg, edit_service_duration, service_id, name, volume)


def edit_service_duration(message, service_id, name, volume):
    duration = message.text
    msg = bot.send_message(message.chat.id, "قیمت سرویس را وارد کنید:")
    bot.register_next_step_handler(msg, edit_service_price, service_id, name, volume, duration)


def edit_service_price(message, service_id, name, volume, duration):
    try:
        price = int(message.text)
    except:
        msg = bot.send_message(message.chat.id, "❌ قیمت باید عدد باشد، دوباره وارد کنید:")
        bot.register_next_step_handler(msg, edit_service_price, service_id, name, volume, duration)
        return

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE services SET name=?, volume=?, duration=?, price=? WHERE id=?",
        (name, volume, duration, price, service_id)
    )
    conn.commit()
    conn.close()

    bot.send_message(message.chat.id, f"✅ سرویس {name} با موفقیت ویرایش شد")

    # fix message is not modified: use send_message
    bot.send_message(
        message.chat.id,
        "🛒 <b>مدیریت سرویس‌ها</b>\n\nیکی از گزینه‌ها را انتخاب کنید:",
        reply_markup=admin_services_menu()
    )


# ---------- Delete service ----------
@bot.callback_query_handler(func=lambda c: c.data == "service_delete")
def service_delete(call):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM services")
    services = cursor.fetchall()
    conn.close()

    if not services:
        bot.answer_callback_query(call.id, "❌ سرویسی وجود ندارد")
        return

    bot.send_message(
        call.message.chat.id,
        "🗑 <b>انتخاب سرویس برای حذف</b>",
        reply_markup=services_list_keyboard(services, "delete")
    )


@bot.callback_query_handler(func=lambda c: c.data.startswith("delete_"))
def delete_service_confirm(call):
    service_id = int(call.data.split("_")[1])
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM services WHERE id=?", (service_id,))
    conn.commit()
    conn.close()

    bot.answer_callback_query(call.id, "✅ سرویس حذف شد")
    # fix message is not modified: send_message instead of admin_services(call)
    bot.send_message(
        call.message.chat.id,
        "🛒 <b>مدیریت سرویس‌ها</b>\n\nیکی از گزینه‌ها را انتخاب کنید:",
        reply_markup=admin_services_menu()
    )


# ------------------------------
# Handler عمومی برای back
# ------------------------------
@bot.callback_query_handler(func=lambda c: c.data == "admin_menu")
def admin_back_to_main(call):
    bot.send_message(
        call.message.chat.id,
        "👑 <b>پنل مدیریت</b>\n\nلطفاً یکی از گزینه‌های مدیریتی را انتخاب کنید:",
        reply_markup=admin_main_menu()
    )

# ------------------------------
# فیلتر رسیدها
# ------------------------------
@bot.callback_query_handler(func=lambda c: c.data == "receipts_pending")
def receipts_pending(call):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM receipts WHERE status='pending'")
    receipts = cursor.fetchall()
    conn.close()

    if not receipts:
        bot.send_message(call.message.chat.id, "📭 هیچ رسیدی در حال بررسی وجود ندارد")
        return

    for r in receipts:
        bot.send_photo(call.message.chat.id, r["photo_id"],
            caption=f"📥 کاربر: {r['user_id']}\n🕒 {r['created_at']}",
            reply_markup=receipt_admin_action(r["id"])
        )


@bot.callback_query_handler(func=lambda c: c.data.startswith("receipt_approve_"))
def receipt_approve(call):
    receipt_id = int(call.data.split("_")[-1])
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM receipts WHERE id=?", (receipt_id,))
    r = cursor.fetchone()
    if not r:
        conn.close()
        return

    cursor.execute("UPDATE receipts SET status='approved' WHERE id=?", (receipt_id,))
    conn.commit()
    conn.close()

    bot.edit_message_caption(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        caption=call.message.caption + "\n✅ تایید شد"
    )

    bot.send_message(r["user_id"], "🎉 رسید شما تأیید شد، سرویس شما آماده است")
    

@bot.callback_query_handler(func=lambda c: c.data.startswith("receipt_reject_"))
def receipt_reject(call):
    receipt_id = int(call.data.split("_")[-1])
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM receipts WHERE id=?", (receipt_id,))
    r = cursor.fetchone()
    if not r:
        conn.close()
        return

    cursor.execute("UPDATE receipts SET status='rejected' WHERE id=?", (receipt_id,))
    conn.commit()
    conn.close()

    bot.edit_message_caption(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        caption=call.message.caption + "\n❌ رد شد"
    )

    bot.send_message(r["user_id"], "⚠️ رسید شما رد شد، لطفاً بررسی و دوباره ارسال کنید")
    
    
def process_receipt_reply(message, receipt_id):
    response_text = message.text
    responded_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT user_id FROM receipts WHERE id=?",
        (receipt_id,)
    )
    r = cursor.fetchone()

    if not r:
        conn.close()
        bot.send_message(message.chat.id, "❌ رسید یافت نشد")
        return

    cursor.execute("""
        UPDATE receipts
        SET status='answered',
            admin_response=?,
            responded_at=?
        WHERE id=?
    """, (response_text, responded_at, receipt_id))

    conn.commit()
    conn.close()

    # ارسال پاسخ به کاربر
    bot.send_message(
        r["user_id"],
        f"💬 پاسخ پشتیبانی:\n\n{response_text}"
    )

    bot.send_message(message.chat.id, "✅ پاسخ برای کاربر ارسال شد")

@bot.callback_query_handler(func=lambda c: c.data.startswith("receipt_reply_"))
def receipt_reply(call):
    receipt_id = int(call.data.split("_")[-1])
    msg = bot.send_message(
        call.message.chat.id,
        "✍️ متن پاسخ به کاربر را وارد کنید:"
    )
    bot.register_next_step_handler(msg, process_receipt_reply, receipt_id)

@bot.callback_query_handler(func=lambda c: c.data == "admin_receipts")
def admin_receipts(call):
    bot.send_message(
        call.message.chat.id,
        "🧾 <b>رسیدهای پرداخت</b>\n\nانتخاب کنید:",
        reply_markup=receipt_admin_filter_menu()
    )


@bot.callback_query_handler(func=lambda c: c.data == "receipts_answered")
def receipts_answered(call):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM receipts
        WHERE status IN ('answered', 'rejected', 'approved')
        ORDER BY responded_at DESC
    """)
    receipts = cursor.fetchall()
    conn.close()

    if not receipts:
        bot.send_message(
            call.message.chat.id,
            "📭 هیچ رسید پاسخ‌داده‌شده‌ای وجود ندارد",
            reply_markup=receipt_admin_filter_menu()
        )
        return

    for r in receipts:
        caption = (
            f"👤 کاربر: {r['user_id']}\n"
            f"🕒 ارسال: {r['created_at']}\n"
        )

        if r["responded_at"]:
            caption += f"⏱ پاسخ: {r['responded_at']}\n"

        if r["admin_response"]:
            caption += f"\n💬 پاسخ ادمین:\n{r['admin_response']}"

        if r["status"] == "rejected":
            caption += "\n\n❌ وضعیت: رد شده"
        elif r["status"] == "approved":
            caption += "\n\n✅ وضعیت: تأیید شده"
        else:
            caption += "\n\n✉️ وضعیت: پاسخ داده شده"

        bot.send_photo(
            call.message.chat.id,
            r["photo_id"],
            caption=caption
        )

@bot.callback_query_handler(func=lambda c: c.data == "admin_support")
def admin_support_menu(call):
    bot.send_message(
        call.message.chat.id,
        "🆘 <b>مدیریت پشتیبانی</b>\n\nانتخاب کنید:",
        reply_markup=support_admin_filter_menu()
    )

@bot.callback_query_handler(func=lambda c: c.data == "support_pending")
def support_pending(call):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM support_tickets
        WHERE status='pending'
        ORDER BY created_at ASC
    """)
    tickets = cursor.fetchall()
    conn.close()

    if not tickets:
        bot.send_message(call.message.chat.id, "📭 تیکت بررسی‌نشده‌ای وجود ندارد")
        return

    for t in tickets:
        bot.send_message(
            call.message.chat.id,
            f"🆘 <b>درخواست پشتیبانی</b>\n\n"
            f"👤 کاربر: <code>{t['user_id']}</code>\n"
            f"🕒 {t['created_at']}\n\n"
            f"💬 پیام:\n{t['message']}",
            reply_markup=support_admin_action(t["id"])
        )

@bot.callback_query_handler(func=lambda c: c.data.startswith("support_reply_"))
def support_reply(call):
    ticket_id = int(call.data.split("_")[-1])
    msg = bot.send_message(call.message.chat.id, "✍️ پاسخ خود را بنویسید:")
    bot.register_next_step_handler(msg, process_support_reply, ticket_id)

def process_support_reply(message, ticket_id):
    response = message.text
    responded_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT user_id FROM support_tickets WHERE id=?",
        (ticket_id,)
    )
    t = cursor.fetchone()

    if not t:
        conn.close()
        return

    cursor.execute("""
        UPDATE support_tickets
        SET status='answered',
            admin_response=?,
            responded_at=?
        WHERE id=?
    """, (response, responded_at, ticket_id))

    # ✅ پاک کردن state کاربر
    cursor.execute(
        "DELETE FROM user_states WHERE user_id=?",
        (t["user_id"],)
    )

    conn.commit()
    conn.close()

    bot.send_message(
        t["user_id"],
        f"💬 <b>پاسخ پشتیبانی</b>\n\n{response}"
    )

    bot.send_message(message.chat.id, "✅ پاسخ ارسال شد")


@bot.callback_query_handler(func=lambda c: c.data.startswith("support_reject_"))
def support_reject(call):
    ticket_id = int(call.data.split("_")[-1])
    responded_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT user_id FROM support_tickets WHERE id=?",
        (ticket_id,)
    )
    t = cursor.fetchone()

    if not t:
        conn.close()
        return

    cursor.execute("""
        UPDATE support_tickets
        SET status='rejected',
            responded_at=?
        WHERE id=?
    """, (responded_at, ticket_id))

    # ✅ پاک کردن state کاربر
    cursor.execute(
        "DELETE FROM user_states WHERE user_id=?",
        (t["user_id"],)
    )

    conn.commit()
    conn.close()

    bot.send_message(
        t["user_id"],
        "❌ درخواست پشتیبانی شما رد شد.\nدر صورت نیاز، مجدد پیام ارسال کنید."
    )

    bot.answer_callback_query(call.id, "رد شد")


@bot.callback_query_handler(func=lambda c: c.data == "support_answered")
def support_answered(call):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM support_tickets
        WHERE status IN ('answered', 'rejected')
        ORDER BY responded_at DESC
    """)
    tickets = cursor.fetchall()
    conn.close()

    if not tickets:
        bot.send_message(call.message.chat.id, "📭 تیکت پاسخ‌داده‌شده‌ای وجود ندارد")
        return

    for t in tickets:
        text = (
            f"👤 کاربر: <code>{t['user_id']}</code>\n"
            f"🕒 ارسال: {t['created_at']}\n"
        )

        if t["responded_at"]:
            text += f"⏱ پاسخ: {t['responded_at']}\n"

        if t["admin_response"]:
            text += f"\n💬 پاسخ:\n{t['admin_response']}"

        if t["status"] == "rejected":
            text += "\n\n❌ وضعیت: رد شده"
        else:
            text += "\n\n✅ وضعیت: پاسخ داده شده"

        bot.send_message(call.message.chat.id, text)
