from telegram import Update
from telegram.ext import ContextTypes
from keyboards.news import NEWS_ACTIONS_KB, NEWS_EDIT_KB
from keyboards.main import main_menu
from config import ADMIN_CHAT_ID

from utils.db import (
    db_add_news,
    db_get_news,
    db_get_news_by_id,
    db_delete_news,
    db_update_news,
    db_get_subscribers,
)


# ───────── ПОКАЗ НОВОСТЕЙ ─────────
async def show_news(update: Update, context: ContextTypes.DEFAULT_TYPE):
    rows = db_get_news()

    if not rows:
        await update.message.reply_text("📰 Пока новостей нет.")
        return

    for n in rows:
        text = f"*{n['title']}*\n\n{n['text']}"
        if n["link"]:
            text += f"\n\n🔗 {n['link']}"

        if n["photo"]:
            await update.message.reply_photo(n["photo"], caption=text, parse_mode="Markdown")
        else:
            await update.message.reply_text(text, parse_mode="Markdown")


# ───────── ПРЕДПРОСМОТР ─────────
async def show_preview(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message
    text = f"📰 Предпросмотр\n\n{context.user_data['title']}\n\n{context.user_data['text']}"

    if context.user_data.get("link"):
        text += f"\n\n🔗 {context.user_data['link']}"

    if context.user_data.get("photo"):
        await msg.reply_photo(context.user_data["photo"], caption=text, reply_markup=NEWS_ACTIONS_KB)
    else:
        await msg.reply_text(text, reply_markup=NEWS_ACTIONS_KB)


# ───────── РАССЫЛКА ─────────
async def broadcast_news(context: ContextTypes.DEFAULT_TYPE, item):
    subs = db_get_subscribers()
    text = f"{item['title']}\n\n{item['text']}"

    for uid in subs:
        try:
            if item["photo"]:
                await context.bot.send_photo(uid, item["photo"], caption=text)
            else:
                await context.bot.send_message(uid, text)
        except:
            pass


# ───────── FLOW ─────────
async def handle_news_flow(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message
    if not msg:
        return False

    text = msg.text or ""
    is_admin = update.effective_user.id == ADMIN_CHAT_ID

    # ───── ПУБЛИКАЦИЯ ─────
    if text == "✅ Опубликовать":
        db_add_news(
            context.user_data["title"],
            context.user_data["text"],
            context.user_data.get("photo"),
            context.user_data.get("link")
        )
        context.user_data.clear()
        await msg.reply_text("✅ Новость опубликована", reply_markup=main_menu(is_admin))
        return True

    # ───── ОТМЕНА ─────
    if text == "❌ Отмена":
        context.user_data.clear()
        await msg.reply_text("❌ Отменено", reply_markup=main_menu(is_admin))
        return True

    # ───── РЕДАКТИРОВАНИЕ ─────
    if context.user_data.get("admin_mode") == "editing":
        field = context.user_data["edit_field"]
        item = context.user_data["edit_item"]
        db_update_news(item["id"], field, text)
        context.user_data.clear()
        await msg.reply_text("Обновлено", reply_markup=main_menu(is_admin))
        return True

    # ───── ВЫБОР ПОЛЯ ─────
    if text == "Заголовок":
        context.user_data["edit_field"] = "title"
        return True
    if text == "Описание":
        context.user_data["edit_field"] = "text"
        return True
    if text == "Ссылка":
        context.user_data["edit_field"] = "link"
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
        await msg.reply_text("Фото или -")
        return True

    if step == "photo":
        if msg.photo:
            context.user_data["photo"] = msg.photo[-1].file_id
        context.user_data["news_step"] = "link"
        await msg.reply_text("Ссылка или -")
        return True

    if step == "link":
        context.user_data["link"] = None if text == "-" else text
        context.user_data.pop("news_step", None)
        await show_preview(update, context)
        return True

    return False
