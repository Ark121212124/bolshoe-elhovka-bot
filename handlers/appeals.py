from telegram import Update
from telegram.ext import ContextTypes
from config import ADMIN_CHAT_ID


async def start_appeal(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.clear()
    context.user_data["appeal_step"] = "fio"

    await update.message.reply_text("✉ Введите *ФИО*:", parse_mode="Markdown")


async def appeals_text_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    step = context.user_data.get("appeal_step")
    if not step:
        return False

    text = update.message.text

    if step == "fio":
        context.user_data["fio"] = text
        context.user_data["appeal_step"] = "phone"
        await update.message.reply_text("📞 Введите номер телефона:")
        return True

    if step == "phone":
        context.user_data["phone"] = text
        context.user_data["appeal_step"] = "text"
        await update.message.reply_text("📝 Опишите суть обращения:")
        return True

    if step == "text":
        fio = context.user_data["fio"]
        phone = context.user_data["phone"]
        message = text

        # 📩 админу
        await context.bot.send_message(
            ADMIN_CHAT_ID,
            f"📩 *Новое обращение*\n\n"
            f"👤 ФИО: {fio}\n"
            f"📞 Телефон: {phone}\n\n"
            f"📝 {message}",
            parse_mode="Markdown"
        )

        context.user_data.clear()
        await update.message.reply_text("✅ Ваше обращение отправлено. Спасибо!")
        return True

    return False
