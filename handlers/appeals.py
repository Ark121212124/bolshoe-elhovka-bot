from telegram import Update
from telegram.ext import ContextTypes


async def start_appeal(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.clear()
    context.user_data["appeal_mode"] = True

    await update.message.reply_text(
        "✉ Напишите ваше обращение одним сообщением."
    )


async def appeals_text_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.user_data.get("appeal_mode"):
        return False

    # тут можно потом сохранять в файл
    context.user_data.clear()

    await update.message.reply_text(
        "✅ Ваше обращение принято. Спасибо!"
    )
    return True
