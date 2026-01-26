import json
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ContextTypes

FILE = "storage/news.json"

ACTIONS_KB = ReplyKeyboardMarkup(
    [["✅ Опубликовать"], ["✏️ Редактировать"], ["❌ Отмена"]],
    resize_keyboard=True
)

EDIT_KB = ReplyKeyboardMarkup(
    [["📝 Заголовок", "📄 Описание"],
     ["🖼 Фото", "🔗 Ссылка"],
     ["🔙 Назад"]],
    resize_keyboard=True
)


def load():
    try:
        with open(FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return []


def save(data):
    with open(FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def preview(data):
    text = f"*{data['title']}*\n\n{data['text']}"
    if data.get("link"):
        text += f"\n\n🔗 {data['link']}"
    return text


async def show_news(update: Update, context: ContextTypes.DEFAULT_TYPE):
    news = load()
    if not news:
        await update.message.reply_text("📰 Пока новостей нет.")
        return

    for n in news:
        if n.get("photo"):
            await update.message.reply_photo(n["photo"], caption=preview(n), parse_mode="Markdown")
        else:
            await update.message.reply_text(preview(n), parse_mode="Markdown")


async def news_text_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    step = context.user_data.get("news_step")

    # ───── СОЗДАНИЕ ─────
    if step == "title":
        context.user_data["title"] = text
        context.user_data["news_step"] = "text"
        await update.message.reply_text("📄 Введите описание:")
        return True

    if step == "text":
        context.user_data["text"] = text
        context.user_data["news_step"] = "photo"
        await update.message.reply_text("🖼 Отправьте фото или `-`", parse_mode="Markdown")
        return True

    if step == "photo":
        if update.message.photo:
            context.user_data["photo"] = update.message.photo[-1].file_id
        context.user_data["news_step"] = "link"
        await update.message.reply_text("🔗 Введите ссылку или `-`")
        return True

    if step == "link":
        context.user_data["link"] = None if text == "-" else text
        context.user_data["news_step"] = "preview"

        data = context.user_data
        if data.get("photo"):
            await update.message.reply_photo(
                data["photo"],
                caption=preview(data),
                parse_mode="Markdown",
                reply_markup=ACTIONS_KB
            )
        else:
            await update.message.reply_text(preview(data), parse_mode="Markdown", reply_markup=ACTIONS_KB)
        return True

    # ───── ДЕЙСТВИЯ ─────
    if text == "✅ Опубликовать":
        news = load()
        news.append({
            "title": context.user_data["title"],
            "text": context.user_data["text"],
            "photo": context.user_data.get("photo"),
            "link": context.user_data.get("link"),
        })
        save(news)
        context.user_data.clear()
        await update.message.reply_text("✅ Новость опубликована")
        return True

    if text == "❌ Отмена":
        context.user_data.clear()
        await update.message.reply_text("❌ Отменено")
        return True

    if text == "✏️ Редактировать":
        context.user_data["news_step"] = "edit"
        await update.message.reply_text("✏️ Что редактировать?", reply_markup=EDIT_KB)
        return True

    # ───── РЕДАКТИРОВАНИЕ ─────
    if step == "edit":
        if text == "📝 Заголовок":
            context.user_data["news_step"] = "edit_title"
            await update.message.reply_text("Введите новый заголовок:")
            return True

        if text == "📄 Описание":
            context.user_data["news_step"] = "edit_text"
            await update.message.reply_text("Введите новое описание:")
            return True

        if text == "🖼 Фото":
            context.user_data["news_step"] = "edit_photo"
            await update.message.reply_text("Отправьте новое фото:")
            return True

        if text == "🔗 Ссылка":
            context.user_data["news_step"] = "edit_link"
            await update.message.reply_text("Введите новую ссылку или `-`:")
            return True

    if step == "edit_title":
        context.user_data["title"] = text

    elif step == "edit_text":
        context.user_data["text"] = text

    elif step == "edit_photo" and update.message.photo:
        context.user_data["photo"] = update.message.photo[-1].file_id

    elif step == "edit_link":
        context.user_data["link"] = None if text == "-" else text

    else:
        return False

    # после любого редактирования → предпросмотр
    context.user_data["news_step"] = "preview"
    data = context.user_data

    if data.get("photo"):
        await update.message.reply_photo(
            data["photo"],
            caption=preview(data),
            parse_mode="Markdown",
            reply_markup=ACTIONS_KB
        )
    else:
        await update.message.reply_text(preview(data), parse_mode="Markdown", reply_markup=ACTIONS_KB)

    return True
