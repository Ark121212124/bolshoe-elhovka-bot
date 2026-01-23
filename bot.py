from telegram.ext import Application, CallbackQueryHandler, CommandHandler
from config import TOKEN

from handlers.start import start
from handlers.menu import menu_handler
from handlers.news import news_callbacks
from handlers.contacts import contacts_callbacks
from handlers.appeals import appeals_callbacks
from handlers.subscriptions import subscriptions_callbacks


def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))

    app.add_handler(CallbackQueryHandler(menu_handler, pattern="^menu_"))
    app.add_handler(CallbackQueryHandler(news_callbacks, pattern="^news_"))
    app.add_handler(CallbackQueryHandler(contacts_callbacks, pattern="^contacts_"))
    app.add_handler(CallbackQueryHandler(appeals_callbacks, pattern="^appeal_"))
    app.add_handler(CallbackQueryHandler(subscriptions_callbacks, pattern="^sub_"))

    print("🚀 Бот запущен")
    app.run_polling()


if __name__ == "__main__":
    main()
