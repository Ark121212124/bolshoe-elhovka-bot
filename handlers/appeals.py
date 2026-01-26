from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ContextTypes
from config import ADMIN_CHAT_ID
from keyboards.main import main_menu


APPEAL_KB = ReplyKeyboardMarkup(
    [["🔙 В меню"]],
    resize_keyboard=True
)


async def start_appeal(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.clear()
    context.user_data["appeal_step"] = "fio"

    await update.message.reply_text(
        "✉ *Обращение*\n\nВведите ФИО:",
        parse_mode="Markdown",
        reply_markup=APPEAL_KB
    )


async def appeals_text_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    step = context.user_data.get("appeal_step")
    if not step:
        return False

    text = update.message.text

    if text == "🔙 В меню":
        context.user_data.clear()
        await update.message.reply_text(
            "🏛 Главное меню",
            reply_markup=main_menu(update.effective_user.id == ADMIN_CHAT_ID)
        )
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
        await update.message.reply_text("🖼 Отправьте фото или `-`")
        return True

    if step == "photo":
        photo = None
        if update.message.photo:
            photo = update.message.photo[-1].file_id

        data = context.user_data

        msg = (
            "📩 *Новое обращение*\n\n"
            f"👤 ФИО: {data['fio']}\n"
            f"📞 Телефон: {data['phone']}\n\n"
            f"📝 {data['text']}"
        )

        await context.bot.send_message(
            ADMIN_CHAT_ID,
            msg,
            parse_mode="Markdown"
        )

        if photo:
            await context.bot.send_photo(ADMIN_CHAT_ID, photo)

        context.user_data.clear()
        await update.message.reply_text(
            "✅ Обращение отправлено. Спасибо!",
            reply_markup=main_menu(update.effective_user.id == ADMIN_CHAT_ID)
        )
        return True
