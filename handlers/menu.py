from telegram import Update
from telegram.ext import ContextTypes
from keyboards.main import main_menu
from config import ADMIN_CHAT_ID


async def menu_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    is_admin = query.from_user.id == ADMIN_CHAT_ID

    if query.data == "menu_main":
        await query.message.edit_text(
            "🏛 *Главное меню*",
            parse_mode="Markdown",
            reply_markup=main_menu(is_admin)
        )
