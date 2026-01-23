from telegram import InlineKeyboardButton, InlineKeyboardMarkup

def main_menu(is_admin: bool):
    buttons = [
        [InlineKeyboardButton("📰 Новости", callback_data="menu_news")],
        [InlineKeyboardButton("📞 Контакты", callback_data="menu_contacts")],
        [InlineKeyboardButton("✉ Обратная связь", callback_data="menu_appeal")],
        [InlineKeyboardButton("🔔 Оповещения", callback_data="menu_subs")],
    ]

    if is_admin:
        buttons.insert(1, [InlineKeyboardButton("➕ Добавить новость", callback_data="menu_add_news")])

    return InlineKeyboardMarkup(buttons)
