from telegram import Update
from telegram.ext import ContextTypes
from keyboards.main import main_menu
from config import ADMIN_CHAT_ID


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    is_admin = update.effective_user.id == ADMIN_CHAT_ID

    await update.message.reply_text(
        "🏛 *Большеелховское сельское поселение*\n\nВыберите раздел:",
        parse_mode="Markdown",
        reply_markup=main_menu(is_admin)
    )
