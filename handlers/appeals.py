from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ContextTypes

BACK_KB = ReplyKeyboardMarkup(
    [["🔙 Назад"]],
    resize_keyboard=True
)

async def start_appeal(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.clear()
    context.user_data["appeal_step"] = "fio"

    await update.message.reply_text(
        "✉ Введите *ФИО*:",
        parse_mode="Markdown",
        reply_markup=BACK_KB
    )


async def appeals_text_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    step = context.user_data.get("appeal_step")
    text = update.message.text

    if not step:
        return False

    if text == "🔙 Назад":
        context.user_data.clear()
        return False

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
        await update.message.reply_text(
            "📷 Прикрепите фото или отправьте `-`, если без фото",
            parse_mode="Markdown"
        )
        return True

    return False
