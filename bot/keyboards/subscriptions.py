from telegram import InlineKeyboardMarkup, InlineKeyboardButton

SUB_KB = InlineKeyboardMarkup([
    [InlineKeyboardButton("🔔 Подписаться", callback_data="sub_on")],
    [InlineKeyboardButton("🔕 Отписаться", callback_data="sub_off")],
    [InlineKeyboardButton("⬅ Назад", callback_data="menu_main")],
])
