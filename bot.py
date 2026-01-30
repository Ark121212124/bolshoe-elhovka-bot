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
    print("🤖 Запуск бота...")

    app = Application.builder().token(TOKEN).build()

    # ───── /start ─────
    app.add_handler(CommandHandler("start", start))

    # ───── ВСЕ СООБЩЕНИЯ ─────
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
