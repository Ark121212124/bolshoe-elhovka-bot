from telegram import Update
from telegram.ext import ContextTypes


async def news_callbacks(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # заглушка, чтобы импорт не падал
    return False
