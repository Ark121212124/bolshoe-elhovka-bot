from telegram import Update
from telegram.ext import ContextTypes
from keyboards.contacts import CONTACTS_KB


CONTACTS_TEXT = {
    "contacts_admin": (
        "🏛 *Администрация поселения*\n\n"
        "📍 с. Большая Елховка, ул. Фабричная, 21\n"
        "🕘 Пн–Пт: 08:30–17:30\n"
        "Перерыв: 13:00–14:00\n"
        "Сб–Вс: выходной"
    ),
    "contacts_mfc": (
        "🗂 *МФЦ*\n\n"
        "📍 ул. Фабричная, 21\n"
        "🕘 Пн–Пт: 08:30–17:00\n"
        "Сб–Вс: выходной"
    ),
    "contacts_jkh": (
        "🚰 *МУП ЖКХ Елховское*\n\n"
        "📍 с. Лямбирь, ул. Полевая, 17\n"
        "🕘 Пн–Пт: 08:00–17:00\n"
        "Перерыв: 12:00–13:00"
    ),
    "contacts_uk": (
        "🏢 *УК «Лямбирькомжилсервис»*\n\n"
        "📍 ул. Заводская, 1\n"
        "🕘 Пн–Пт: 07:45–16:30\n"
        "Перерыв: 12:00–13:00"
    ),
    "contacts_hospital": (
        "🏥 *Большеелховская амбулатория*\n\n"
        "📍 ул. Имерякова, 33\n"
        "🕘 Пн–Пт: 09:00–18:00"
    ),
}


async def contacts_callbacks(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data.startswith("contacts_"):
        await query.message.edit_text(
            CONTACTS_TEXT[query.data],
            parse_mode="Markdown",
            reply_markup=CONTACTS_KB
        )
