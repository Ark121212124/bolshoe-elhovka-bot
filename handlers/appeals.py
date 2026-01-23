from telegram import Update
from telegram.ext import ContextTypes


async def start_appeal(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["appeal"] = True
    await update.message.reply_text(
        "✉ Напишите ваше обращение одним сообщением."
    )


async def appeals_text_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.user_data.get("appeal"):
        text = update.message.text
        context.user_data["appeal"] = False

        await update.message.reply_text(
            "✅ Ваше обращение принято. Спасибо!"
        )
        return True

    return False
