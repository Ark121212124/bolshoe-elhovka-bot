import json
from datetime import datetime
from telegram import Update
from telegram.ext import ContextTypes
from keyboards.news import NEWS_ACTIONS_KB, NEWS_EDIT_KB

FILE = "storage/news.json"
SUB_FILE = "storage/subscribers.json"


# ─────────────────────────
# ФАЙЛЫ
# ─────────────────────────

def load_news():
    try:
        with open(FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return []


def save_news(data):
    with open(FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def next_id(news):
    if not news:
        return 1
    return max(n["id"] for n in news) + 1


def load_subs():
    try:
        with open(SUB_FILE, "r") as f:
            return json.load(f)
    except:
        return []


# ─────────────────────────
# ПОКАЗ НОВОСТЕЙ
# ─────────────────────────

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


# ─────────────────────────
# ПРЕДПРОСМОТР
# ─────────────────────────

async def show_preview(update, context):
    msg = update.message

    title = context.user_data.get("title", "")
    text_news = context.user_data.get("text", "")
    link = context.user_data.get("link")
    photo = context.user_data.get("photo")

    caption = f"📰 Предпросмотр\n\n{title}\n\n{text_news}"

    if link:
        caption += f"\n\n🔗 {link}"

    if photo:
        await msg.reply_photo(photo, caption=caption, reply_markup=NEWS_ACTIONS_KB)
    else:
        await msg.reply_text(caption, reply_markup=NEWS_ACTIONS_KB)


# ─────────────────────────
# РАССЫЛКА
# ─────────────────────────

async def broadcast_news(context, item):
    subs = load_subs()
    text = f"{item['title']}\n\n{item['text']}"

    if item.get("link"):
        text += f"\n{item['link']}"

    for uid in subs:
        try:
            if item.get("photo"):
                await context.bot.send_photo(uid, item["photo"], caption=text)
            else:
                await context.bot.send_message(uid, text)
        except:
            pass


# ─────────────────────────
# ГЛАВНЫЙ FLOW
# ─────────────────────────

async def handle_news_flow(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message
    text = msg.text if msg.text else ""

    # ───── ПУБЛИКАЦИЯ ─────
    if text == "✅ Опубликовать":
        news = load_news()

        item = {
            "id": next_id(news),
            "title": context.user_data.get("title"),
            "text": context.user_data.get("text"),
            "photo": context.user_data.get("photo"),
            "link": context.user_data.get("link"),
            "date": datetime.now().strftime("%Y-%m-%d")
        }

        news.append(item)
        save_news(news)

        context.user_data.clear()
        await msg.reply_text("✅ Новость опубликована")
        return True

    # ───── ОТМЕНА ─────
    if text == "❌ Отмена":
        context.user_data.clear()
        await msg.reply_text("❌ Отменено")
        return True

    # ───── РЕДАКТИРОВАНИЕ ПОЛЕЙ ─────
    if text == "✏ Редактировать":
        await msg.reply_text("Что редактировать?", reply_markup=NEWS_EDIT_KB)
        return True

    if text == "📝 Заголовок":
        context.user_data["news_step"] = "edit_title"
        await msg.reply_text("Введите новый заголовок:")
        return True

    if text == "📄 Описание":
        context.user_data["news_step"] = "edit_text"
        await msg.reply_text("Введите новое описание:")
        return True

    if text == "🖼 Фото":
        context.user_data["news_step"] = "edit_photo"
        await msg.reply_text("Отправьте новое фото или -")
        return True

    if text == "🔗 Ссылку":
        context.user_data["news_step"] = "edit_link"
        await msg.reply_text("Введите новую ссылку или -")
        return True

    # ───── ШАГИ ─────
    step = context.user_data.get("news_step")
    if not step:
        return False

    # СОЗДАНИЕ
    if step == "title":
        context.user_data["title"] = text
        context.user_data["news_step"] = "text"
        await msg.reply_text("Введите описание:")
        return True

    if step == "text":
        context.user_data["text"] = text
        context.user_data["news_step"] = "photo"
        await msg.reply_text("Отправьте фото или -")
        return True

    if step == "photo":
        if msg.photo:
            context.user_data["photo"] = msg.photo[-1].file_id
        else:
            context.user_data["photo"] = None

        context.user_data["news_step"] = "link"
        await msg.reply_text("Введите ссылку или -")
        return True

    if step == "link":
        context.user_data["link"] = None if text == "-" else text
        context.user_data.pop("news_step", None)
        await show_preview(update, context)
        return True

    # EDIT TITLE
    if step == "edit_title":
        context.user_data["title"] = text
        context.user_data.pop("news_step", None)
        await show_preview(update, context)
        return True

    # EDIT TEXT
    if step == "edit_text":
        context.user_data["text"] = text
        context.user_data.pop("news_step", None)
        await show_preview(update, context)
        return True

    # EDIT PHOTO
    if step == "edit_photo":
        if msg.photo:
            context.user_data["photo"] = msg.photo[-1].file_id
        else:
            context.user_data["photo"] = None

        context.user_data.pop("news_step", None)
        await show_preview(update, context)
        return True

    # EDIT LINK
    if step == "edit_link":
        context.user_data["link"] = None if text == "-" else text
        context.user_data.pop("news_step", None)
        await show_preview(update, context)
        return True

    return False
