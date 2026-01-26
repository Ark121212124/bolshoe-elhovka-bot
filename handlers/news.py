import json
from telegram import Update
from telegram.ext import ContextTypes
from keyboards.news import NEWS_ACTIONS_KB, NEWS_EDIT_KB

FILE = "storage/news.json"


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
        await update.message.reply_text("📰 Пока новостей нет.")
        return

    for n in news:
        text = f"*{n['title']}*\n\n{n['text']}"
        if n.get("link"):
            text += f"\n\n🔗 {n['link']}"

        if n.get("photo"):
            await update.message.reply_photo(n["photo"], caption=text, parse_mode="Markdown")
        else:
            await update.message.reply_text(text, parse_mode="Markdown")


# ─────────────────────────────
# 🔥 ГЛАВНЫЙ ОБРАБОТЧИК НОВОСТЕЙ
# ─────────────────────────────
async def handle_news_flow(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message
    text = msg.text if msg and msg.text else ""

    # ───── КНОПКИ РАБОТАЮТ ВСЕГДА ─────
    if text == "✅ Опубликовать":
        news = load_news()
        news.append({
            "title": context.user_data.get("title"),
            "text": context.user_data.get("text"),
            "photo": context.user_data.get("photo"),
            "link": context.user_data.get("link"),
        })
        save_news(news)
        context.user_data.clear()
        await msg.reply_text("✅ Новость опубликована")
        return True

    if text == "❌ Отмена":
        context.user_data.clear()
        await msg.reply_text("❌ Добавление новости отменено")
        return True

    if text == "✏ Редактировать":
        await msg.reply_text("✏ Что редактировать?", reply_markup=NEWS_EDIT_KB)
        return True

    if text == "📝 Заголовок":
        context.user_data["news_step"] = "title"
        await msg.reply_text("📝 Введите новый заголовок:")
        return True

    if text == "📄 Описание":
        context.user_data["news_step"] = "text"
        await msg.reply_text("📄 Введите новое описание:")
        return True

    if text == "🖼 Фото":
        context.user_data["news_step"] = "photo"
        await msg.reply_text("🖼 Отправьте новое фото или `-`")
        return True

    if text == "🔗 Ссылку":
        context.user_data["news_step"] = "link"
        await msg.reply_text("🔗 Введите новую ссылку или `-`")
        return True

    # ───── ВВОД ДАННЫХ ПО ШАГАМ ─────
    step = context.user_data.get("news_step")
    if not step:
        return False

    if step == "title":
        context.user_data["title"] = text
        context.user_data["news_step"] = "text"
        await msg.reply_text("📄 Введите описание:")
        return True

    if step == "text":
        context.user_data["text"] = text
        context.user_data["news_step"] = "photo"
        await msg.reply_text("🖼 Отправьте фото или `-`")
        return True

    if step == "photo":
        if msg.photo:
            context.user_data["photo"] = msg.photo[-1].file_id
        else:
            context.user_data["photo"] = None

        context.user_data["news_step"] = "link"
        await msg.reply_text("🔗 Введите ссылку или `-`")
        return True

    if step == "link":
        context.user_data["link"] = None if text == "-" else text
        context.user_data.pop("news_step", None)
        await show_preview(update, context)
        return True

    return False


async def show_preview(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        f"📰 Предпросмотр\n\n"
        f"{context.user_data.get('title')}\n\n"
        f"{context.user_data.get('text')}"
    )

    if context.user_data.get("link"):
        text += f"\n\n🔗 {context.user_data['link']}"

    if context.user_data.get("photo"):
        await update.message.reply_photo(
            context.user_data["photo"],
            caption=text,
            reply_markup=NEWS_ACTIONS_KB
        )
    else:
        await update.message.reply_text(
            text,
            reply_markup=NEWS_ACTIONS_KB
        )
