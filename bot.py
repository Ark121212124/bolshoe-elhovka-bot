from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
)

from config import TOKEN
from handlers.start import start
from handlers.menu import text_menu_handler
from utils.db import init_db


def main():
    print("🔧 Инициализация базы...")
    init_db()

    print("🤖 Запуск бота...")
    app = Application.builder().token(TOKEN).build()

    # /start
    app.add_handler(CommandHandler("start", start))

    # ВСЕ сообщения кроме команд
    app.add_handler(
        MessageHandler(
            filters.ALL & ~filters.COMMAND,
            text_menu_handler
        )
    )

    print("🚀 Bot started!")

    app.run_polling(
        drop_pending_updates=True
    )


if __name__ == "__main__":
    main()
