from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ContextTypes

# ВРЕМЕННОЕ ХРАНИЛИЩЕ ПОДПИСЧИКОВ В ПАМЯТИ
SUBSCRIBERS = set()

SUB_MENU = ReplyKeyboardMarkup(
    [
        ["🔔 Подписаться"],
        ["🔕 Отписаться"],
        ["🔙 Назад"],
    ],
    resize_keyboard=True
)


async def subscriptions_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.clear()
    context.user_data["subs_mode"] = True

    await update.message.reply_text(
        "🔔 Оповещения\n\nВыберите действие:",
        reply_markup=SUB_MENU
    )


async def subscriptions_text_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.user_data.get("subs_mode"):
        return False

    text = update.message.text
    uid = update.effective_user.id

    # НАЗАД
    if text == "🔙 Назад":
        context.user_data.clear()
        return False

    # ПОДПИСКА
    if text == "🔔 Подписаться":
        SUBSCRIBERS.add(uid)
        await update.message.reply_text("✅ Вы подписались на новости")
        return True

    # ОТПИСКА
    if text == "🔕 Отписаться":
        SUBSCRIBERS.discard(uid)
        await update.message.reply_text("❌ Вы отписались от новостей")
        return True

    return True
