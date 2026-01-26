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


# 🔥 ГЛАВНЫЙ ОБРАБОТЧИК
async def handle_news_flow(update: Update, context: ContextTypes.DEFAULT_TYPE):
    step = context.user_data.get("news_step")
    if not step:
        return False

    msg = update.message
    text = msg.text if msg else ""

    # ─── ЗАГОЛОВОК
    if step == "title":
        context.user_data["title"] = text
        context.user_data["news_step"] = "text"
        await msg.reply_text("📄 Введите описание:")
        return True

    # ─── ТЕКСТ
    if step == "text":
        context.user_data["text"] = text
        context.user_data["news_step"] = "photo"
        await msg.reply_text("🖼 Отправьте фото или `-`")
        return True

    # ─── ФОТО
    if step == "photo":
        if msg.photo:
            context.user_data["photo"] = msg.photo[-1].file_id
        else:
            context.user_data["photo"] = None

        context.user_data["news_step"] = "link"
        await msg.reply_text("🔗 Введите ссылку или `-`")
        return True

    # ─── ССЫЛКА → ПРЕДПРОСМОТР
    if step == "link":
        context.user_data["link"] = None if text == "-" else text
        context.user_data["news_step"] = "preview"

        await show_preview(update, context)
        return True

    # ─── ДЕЙСТВИЯ
    if text == "✅ Опубликовать":
        news = load_news()
        news.append({
            "title": context.user_data["title"],
            "text": context.user_data["text"],
            "photo": context.user_data["photo"],
            "link": context.user_data["link"],
        })
        save_news(news)
        context.user_data.clear()
        await msg.reply_text("✅ Новость опубликована")
        return True

    if text == "❌ Отмена":
        context.user_data.clear()
        await msg.reply_text("❌ Отменено")
        return True

    return False


async def show_preview(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        f"📰 *Предпросмотр*\n\n"
        f"*{context.user_data['title']}*\n\n"
        f"{context.user_data['text']}"
    )

    if context.user_data.get("link"):
        text += f"\n\n🔗 {context.user_data['link']}"

    if context.user_data.get("photo"):
        await update.message.reply_photo(
            context.user_data["photo"],
            caption=text,
            parse_mode="Markdown",
            reply_markup=NEWS_ACTIONS_KB
        )
    else:
        await update.message.reply_text(
            text,
            parse_mode="Markdown",
            reply_markup=NEWS_ACTIONS_KB
        )
