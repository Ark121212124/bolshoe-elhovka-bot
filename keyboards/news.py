from telegram import ReplyKeyboardMarkup

NEWS_ACTIONS_KB = ReplyKeyboardMarkup(
    [
        ["✅ Опубликовать"],
        ["✏ Редактировать"],
        ["❌ Отмена"],
        ["🔙 В меню"],
    ],
    resize_keyboard=True
)

NEWS_EDIT_KB = ReplyKeyboardMarkup(
    [
        ["📝 Заголовок"],
        ["📄 Описание"],
        ["🖼 Фото"],
        ["🔗 Ссылку"],
        ["🔙 Назад"],
    ],
    resize_keyboard=True
)
