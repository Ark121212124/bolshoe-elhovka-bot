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
    # ───────── БАЗА ДАННЫХ ─────────
    init_db()

    # ───────── ПРИЛОЖЕНИЕ ─────────
    app = Application.builder().token(TOKEN).build()

    # ───────── /START ─────────
    app.add_handler(CommandHandler("start", start))

    # ───────── ВСЕ СООБЩЕНИЯ ─────────
    app.add_handler(
        MessageHandler(
            filters.ALL & ~filters.COMMAND,
            text_menu_handler
        )
    )

    print("🚀 Bot started...")

    # ───────── ЗАПУСК ─────────
    app.run_polling(
        allowed_updates=None,
        drop_pending_updates=True
    )


if __name__ == "__main__":
    main()
