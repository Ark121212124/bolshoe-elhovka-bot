import json
from datetime import datetime
from telegram import Update
from telegram.ext import ContextTypes
from keyboards.news import NEWS_ACTIONS_KB, NEWS_EDIT_KB, NEWS_ADMIN_KB

FILE = "storage/news.json"
SUB_FILE = "storage/subscribers.json"


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


async def show_preview(update, context):
    msg = update.message
    text = f"📰 Предпросмотр\n\n{context.user_data['title']}\n\n{context.user_data['text']}"

    if context.user_data.get("link"):
        text += f"\n\n🔗 {context.user_data['link']}"

    if context.user_data.get("photo"):
        await msg.reply_photo(context.user_data["photo"], caption=text, reply_markup=NEWS_ACTIONS_KB)
    else:
        await msg.reply_text(text, reply_markup=NEWS_ACTIONS_KB)


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


async def handle_news_flow(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message
    text = msg.text if msg.text else ""

    # ───── ПУБЛИКАЦИЯ ─────
    if text == "✅ Опубликовать":
        news = load_news()
        item = {
            "id": next_id(news),
            "title": context.user_data["title"],
            "text": context.user_data["text"],
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

    # ───── ВЫБОР НОВОСТИ АДМИНОМ ─────
    if text == "✏ Редактировать новость":
        news = load_news()
        for n in news:
            await msg.reply_text(f"{n['id']}. {n['title']}")
        context.user_data["admin_mode"] = "edit_select"
        return True

    if text == "🗑 Удалить новость":
        news = load_news()
        for n in news:
            await msg.reply_text(f"{n['id']}. {n['title']}")
        context.user_data["admin_mode"] = "delete_select"
        return True

    if text == "📨 Разослать новость":
        news = load_news()
        for n in news:
            await msg.reply_text(f"{n['id']}. {n['title']}")
        context.user_data["admin_mode"] = "broadcast_select"
        return True

    # ───── АДМИН ВЫБРАЛ ID ─────
    if context.user_data.get("admin_mode"):
        news = load_news()
        try:
            nid = int(text)
        except:
            return True

        item = next((n for n in news if n["id"] == nid), None)
        if not item:
            return True

        mode = context.user_data["admin_mode"]

        if mode == "delete_select":
            news = [n for n in news if n["id"] != nid]
            save_news(news)
            await msg.reply_text("🗑 Удалено")
            context.user_data.clear()
            return True

        if mode == "broadcast_select":
            await broadcast_news(context, item)
            await msg.reply_text("📨 Разослано")
            context.user_data.clear()
            return True

        if mode == "edit_select":
            context.user_data["edit_item"] = item
            context.user_data["admin_mode"] = "editing"
            await msg.reply_text("Что редактировать?", reply_markup=NEWS_EDIT_KB)
            return True

    # ───── СОЗДАНИЕ НОВОСТИ ─────
    step = context.user_data.get("news_step")

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
        context.user_data["news_step"] = "link"
        await msg.reply_text("Введите ссылку или -")
        return True

    if step == "link":
        context.user_data["link"] = None if text == "-" else text
        context.user_data.pop("news_step", None)
        await show_preview(update, context)
        return True

    return False
