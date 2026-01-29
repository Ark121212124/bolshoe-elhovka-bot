from telegram import ReplyKeyboardMarkup

def main_menu(is_admin: bool):
    buttons = [
        ["📰 Новости"],
        ["📞 Контакты"],
        ["✉ Обратная связь"],
        ["🔔 Оповещения"],
    ]

    if is_admin:
        buttons.insert(1, ["➕ Добавить новость"])
        buttons.insert(2, ["🛠 Управление новостями"])
        
    return ReplyKeyboardMarkup(
        buttons,
        resize_keyboard=True,
        one_time_keyboard=False
    )

