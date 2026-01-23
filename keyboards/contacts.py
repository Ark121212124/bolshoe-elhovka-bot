from telegram import InlineKeyboardButton, InlineKeyboardMarkup

CONTACTS_KB = InlineKeyboardMarkup([
    [InlineKeyboardButton("🏛 Администрация", callback_data="contacts_admin")],
    [InlineKeyboardButton("🗂 МФЦ", callback_data="contacts_mfc")],
    [InlineKeyboardButton("🚰 МУП ЖКХ", callback_data="contacts_jkh")],
    [InlineKeyboardButton("🏢 УК", callback_data="contacts_uk")],
    [InlineKeyboardButton("🏥 Амбулатория", callback_data="contacts_hospital")],
    [InlineKeyboardButton("⬅ Назад", callback_data="menu_main")],
])
