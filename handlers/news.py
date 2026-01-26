import json
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ContextTypes

FILE = "storage/news.json"

NEWS_ACTIONS_KB = ReplyKeyboardMarkup(
    [
        ["✅ Опубликовать"],
        ["✏ Редактировать"],
        ["❌ Отмена"],
    ],
    resize_keyboard=True
)

NEWS_EDIT_KB = ReplyKeyboardMarkup(
    [
        ["📝 Заголовок"],
        ["📄 Описание"],
        ["🖼 Фото"],
        ["🔗 Ссылку"],
        ["🔙 В меню"],
    ],
    resize_keyboard=True
)


def load_news():
    try:
        with open(FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return []


def save_news(data):
    with open(FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


async def show_news(update: Update, context: ContextTypes.DEFAULT_TYPE):
    news = load_news()
    if not news:
        await update.message.reply_text("📰 Новостей пока нет.")
        return

    for n in news:
        text = f"*{n['title']}*\n\n{n['text']}"
        if n.get("link"):
            text += f"\n\n🔗 {n['link']}"

        if n.get("photo"):
            await update.message.reply_photo(n["photo"], caption=text, parse_mode="Markdown")
        else:
            await update.message.reply_text(text, parse_mode="Markdown")


async def news_text_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    step = context.user_data.get("news_step")

    if step == "title":
        context.user_data["news_title"] = text
        context.user_data["news_step"] = "text"
        await update.message.reply_text("📄 Введите описание новости:")
        return True

    if step == "text":
        context.user_data["news_text"] = text
        context.user_data["news_step"] = "photo"
        await update.message.reply_text("🖼 Отправьте фото или `-`")
        return True

    if step == "photo":
        if update.message.photo:
            context.user_data["news_photo"] = update.message.photo[-1].file_id
        context.user_data["news_step"] = "link"
        await update.message.reply_text("🔗 Введите ссылку или `-`")
        return True

    if step == "link":
        context.user_data["news_link"] = None if text == "-" else text
        context.user_data["news_step"] = "actions"

        preview = (
            f"*{context.user_data['news_title']}*\n\n"
            f"{context.user_data['news_text']}"
        )
        if context.user_data.get("news_link"):
            preview += f"\n\n🔗 {context.user_data['news_link']}"

        if context.user_data.get("news_photo"):
            await update.message.reply_photo(
                context.user_data["news_photo"],
                caption=preview,
                parse_mode="Markdown",
                reply_markup=NEWS_ACTIONS_KB
            )
        else:
            await update.message.reply_text(
                preview,
                parse_mode="Markdown",
                reply_markup=NEWS_ACTIONS_KB
            )
        return True

    if text == "✅ Опубликовать":
        news = load_news()
        news.append({
            "title": context.user_data["news_title"],
            "text": context.user_data["news_text"],
            "photo": context.user_data.get("news_photo"),
            "link": context.user_data.get("news_link"),
        })
        save_news(news)
        context.user_data.clear()
        await update.message.reply_text("✅ Новость опубликована")
        return True

    if text == "❌ Отмена":
        context.user_data.clear()
        await update.message.reply_text("❌ Добавление отменено")
        return True

    if text == "✏ Редактировать":
        await update.message.reply_text(
            "✏ Что редактировать?",
            reply_markup=NEWS_EDIT_KB
        )
        return True

    if text == "📝 Заголовок":
        context.user_data["news_step"] = "title"
        await update.message.reply_text("Введите новый заголовок:")
        return True

    if text == "📄 Описание":
        context.user_data["news_step"] = "text"
        await update.message.reply_text("Введите новое описание:")
        return True

    if text == "🖼 Фото":
        context.user_data["news_step"] = "photo"
        await update.message.reply_text("Отправьте новое фото:")
        return True

    if text == "🔗 Ссылку":
        context.user_data["news_step"] = "link"
        await update.message.reply_text("Введите новую ссылку или `-`")
        return True

    if text == "🔙 В меню":
        context.user_data.clear()
        await update.message.reply_text("Редактирование отменено")
        return True

    return False
