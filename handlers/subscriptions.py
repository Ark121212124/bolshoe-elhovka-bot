import json
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ContextTypes

FILE = "storage/subscribers.json"

SUB_MENU = ReplyKeyboardMarkup(
    [
        ["🔔 Подписаться"],
        ["🔕 Отписаться"],
        ["🔙 Назад"],
    ],
    resize_keyboard=True
)


def load():
    try:
        with open(FILE, "r") as f:
            return json.load(f)
    except:
        return []


def save(data):
    with open(FILE, "w") as f:
        json.dump(data, f)


async def subscriptions_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🔔 *Оповещения*\n\nВыберите действие:",
        parse_mode="Markdown",
        reply_markup=SUB_MENU
    )


async def subscriptions_text_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    subs = load()
    uid = update.effective_user.id

    if text == "🔔 Подписаться":
        if uid not in subs:
            subs.append(uid)
            save(subs)
        await update.message.reply_text("✅ Вы подписались на новости")
        return True

    if text == "🔕 Отписаться":
        if uid in subs:
            subs.remove(uid)
            save(subs)
        await update.message.reply_text("❌ Вы отписались от новостей")
        return True

    return False
