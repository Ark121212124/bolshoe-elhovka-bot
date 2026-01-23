from telegram import Update
from telegram.ext import ContextTypes

from handlers.contacts import show_contacts, contacts_text_handler
from handlers.appeals import start_appeal, appeals_text_handler
from handlers.subscriptions import subscriptions_menu, subscriptions_text_handler
from handlers.news import show_news, news_text_handler
from keyboards.main import main_menu
from config import ADMIN_CHAT_ID


async def text_menu_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    user_id = update.effective_user.id
    is_admin = user_id == ADMIN_CHAT_ID

    # 🔴 СНАЧАЛА ДИАЛОГИ
    if await news_text_handler(update, context):
        return

    if await appeals_text_handler(update, context):
        return

    if await contacts_text_handler(update, context):
        return

    if await subscriptions_text_handler(update, context):
        return

    # 📋 МЕНЮ
    if text == "📰 Новости":
        await show_news(update, context)
        return

    if text == "➕ Добавить новость" and is_admin:
        context.user_data.clear()
        context.user_data["news_step"] = "title"
        await update.message.reply_text("📝 Введите заголовок новости:")
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

    if text == "🔙 Назад":
        context.user_data.clear()
        await update.message.reply_text(
            "🏛 *Главное меню*",
            parse_mode="Markdown",
            reply_markup=main_menu(is_admin)
        )
        return

    await update.message.reply_text(
        "Пожалуйста, выберите пункт меню 👇",
        reply_markup=main_menu(is_admin)
    )
