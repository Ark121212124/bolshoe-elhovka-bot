from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
)

from config import TOKEN
from handlers.start import start
from handlers.menu import text_menu_handler


def main():
    app = Application.builder().token(TOKEN).build()

    # /start
    app.add_handler(CommandHandler("start", start))

    # ⬇️ ОДИН обработчик: текст + фото + всё остальное
    app.add_handler(
        MessageHandler(filters.ALL & ~filters.COMMAND, text_menu_handler)
    )

    print("🚀 Бот запущен")
    app.run_polling()


if __name__ == "__main__":
    main()
