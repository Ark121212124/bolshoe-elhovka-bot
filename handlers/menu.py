from telegram import Update
from telegram.ext import ContextTypes

async def text_menu_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    if text == "📰 Новости":
        await update.message.reply_text("📰 Загружаю новости…")
        # тут потом вызовешь показ новостей
        return

    if text == "➕ Добавить новость":
        await update.message.reply_text("➕ Добавление новости")
        return

    if text == "📞 Контакты":
        await update.message.reply_text("📞 Контакты организаций")
        return

    if text == "✉ Обратная связь":
        await update.message.reply_text("✉ Напишите ваше обращение")
        return

    if text == "🔔 Оповещения":
        await update.message.reply_text("🔔 Управление оповещениями")
        return
