from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ContextTypes
from config import ADMIN_CHAT_ID

BACK_KB = ReplyKeyboardMarkup([["🔙 В меню"]], resize_keyboard=True)

async def start_appeal(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.clear()
    context.user_data["appeal_step"] = "fio"
    await update.message.reply_text("✉ Введите *ФИО*:", parse_mode="Markdown", reply_markup=BACK_KB)


async def appeals_text_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    step = context.user_data.get("appeal_step")
    if not step:
        return False

    text = update.message.text

    if text == "🔙 В меню":
        context.user_data.clear()
        await update.message.reply_text("🏛 Главное меню")
        return True

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
        context.user_data["text"] = text
        context.user_data["appeal_step"] = "photo"
        await update.message.reply_text("📷 Отправьте фото или `-`", parse_mode="Markdown")
        return True

    if step == "photo":
        photo = update.message.photo[-1].file_id if update.message.photo else None

        msg = (
            f"📩 *Новое обращение*\n\n"
            f"👤 {context.user_data['fio']}\n"
            f"📞 {context.user_data['phone']}\n\n"
            f"📝 {context.user_data['text']}"
        )

        if photo:
            await context.bot.send_photo(ADMIN_CHAT_ID, photo, caption=msg, parse_mode="Markdown")
        else:
            await context.bot.send_message(ADMIN_CHAT_ID, msg, parse_mode="Markdown")

        context.user_data.clear()
        await update.message.reply_text("✅ Обращение отправлено. Спасибо!")
        return True
