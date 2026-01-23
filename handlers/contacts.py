from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ContextTypes


CONTACTS_MENU = ReplyKeyboardMarkup(
    [
        ["🏛 Администрация поселения"],
        ["🗂 МФЦ"],
        ["🚰 МУП ЖКХ Елховское"],
        ["🏢 УК Лямбирькомжилсервис"],
        ["🏥 Большеелховская амбулатория"],
        ["🔙 Назад"],
    ],
    resize_keyboard=True
)


async def show_contacts(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📞 *Контакты организаций*\n\nВыберите организацию:",
        parse_mode="Markdown",
        reply_markup=CONTACTS_MENU
    )


async def contacts_text_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    data = {
        "🏛 Администрация поселения": (
            "🏛 *Администрация поселения*\n\n"
            "📍 с. Большая Елховка, ул. Фабричная, 21\n"
            "🕘 Пн–Пт: 08:30–17:30\n"
            "Перерыв: 13:00–14:00\n"
            "Сб–Вс: выходной"
        ),
        "🗂 МФЦ": (
            "🗂 *МФЦ*\n\n"
            "📍 ул. Фабричная, 21\n"
            "🕘 Пн–Пт: 08:30–17:00\n"
            "Сб–Вс: выходной"
        ),
        "🚰 МУП ЖКХ Елховское": (
            "🚰 *МУП ЖКХ Елховское*\n\n"
            "📍 с. Лямбирь, ул. Полевая, 17\n"
            "🕘 Пн–Пт: 08:00–17:00\n"
            "Перерыв: 12:00–13:00"
        ),
        "🏢 УК Лямбирькомжилсервис": (
            "🏢 *УК Лямбирькомжилсервис*\n\n"
            "📍 ул. Заводская, 1\n"
            "🕘 Пн–Пт: 07:45–16:30\n"
            "Перерыв: 12:00–13:00"
        ),
        "🏥 Большеелховская амбулатория": (
            "🏥 *Большеелховская амбулатория*\n\n"
            "📍 ул. Имерякова, 33\n"
            "🕘 Пн–Пт: 09:00–18:00"
        ),
    }

    if text in data:
        await update.message.reply_text(
            data[text],
            parse_mode="Markdown"
        )
        return True

    return False
