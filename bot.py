from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
)

from config import TOKEN
from handlers.start import start
from handlers.menu import text_menu_handler
from handlers.news import news_photo_handler


def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))

    app.add_handler(MessageHandler(filters.PHOTO, news_photo_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text_menu_handler))

    print("🚀 Бот запущен")
    app.run_polling()


if __name__ == "__main__":
    main()
