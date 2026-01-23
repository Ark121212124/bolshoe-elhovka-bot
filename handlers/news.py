from telegram import Update
from telegram.ext import ContextTypes


async def show_news(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📰 *Новости поселения*\n\n"
        "Пока новостей нет.",
        parse_mode="Markdown"
    )
