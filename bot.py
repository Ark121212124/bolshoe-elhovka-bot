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
    # ───── ИНИЦИАЛИЗАЦИЯ БАЗЫ ДАННЫХ ─────
    init_db()

    # ───── СОЗДАНИЕ ПРИЛОЖЕНИЯ ─────
    app = Application.builder().token(TOKEN).build()

    # ───── КОМАНДЫ ─────
    app.add_handler(CommandHandler("start", start))

    # ───── ОДИН ОБРАБОТЧИК НА ВСЁ ─────
    # Текст, фото, кнопки, всё кроме команд
    app.add_handler(
        MessageHandler(filters.ALL & ~filters.COMMAND, text_menu_handler)
    )

    print("🚀 Бот запущен")
    app.run_polling()


if __name__ == "__main__":
    main()
