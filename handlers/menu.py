from telegram import Update
from telegram.ext import ContextTypes

from handlers.news import show_news
from handlers.contacts import show_contacts
from handlers.appeals import start_appeal
from handlers.subscriptions import subscriptions_menu


async def text_menu_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    if text == "📰 Новости":
        await show_news(update, context)
        return

    if text == "➕ Добавить новость":
        await update.message.reply_text("➕ Функция добавления новости (админ)")
        return

    if text == "📞 Контакты":
        await show_contacts(update, context)
        return

    if text == "✉ Обратная связь":
        await start_appeal(update, context)
        return

    if text == "🔔 Оповещения":
        await subscriptions_menu(update, context)
        return

    # если пользователь написал что-то вручную
    await update.message.reply_text("Пожалуйста, выберите пункт меню 👇")
