from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ContextTypes
from utils.db import get_conn

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
        "🔔 *Оповещения*\n\nВыберите действие:",
        parse_mode="Markdown",
        reply_markup=SUB_MENU
    )


async def subscriptions_text_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.user_data.get("subs_mode"):
        return False

    text = update.message.text
    uid = update.effective_user.id

    conn = get_conn()
    cur = conn.cursor()

    if text == "🔙 Назад":
        context.user_data.clear()
        conn.close()
        return False

    if text == "🔔 Подписаться":
        cur.execute("INSERT OR IGNORE INTO subscribers VALUES (?)", (uid,))
        conn.commit()
        await update.message.reply_text("✅ Вы подписались на новости")
        conn.close()
        return True

    if text == "🔕 Отписаться":
        cur.execute("DELETE FROM subscribers WHERE id=?", (uid,))
        conn.commit()
        await update.message.reply_text("❌ Вы отписались от новостей")
        conn.close()
        return True

    conn.close()
    return True
