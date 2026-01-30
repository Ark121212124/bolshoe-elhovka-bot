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


# ───────────── ПОКАЗ НОВОСТЕЙ ─────────────
async def show_news(update: Update, context: ContextTypes.DEFAULT_TYPE):
    rows = db_get_news()

    if not rows:
        await update.message.reply_text("📰 Пока новостей нет.")
        return

    for n in rows:
        title = n["title"]
        text_news = n["text"]
        photo = n["photo"]
        link = n["link"]

        text = f"*{title}*\n\n{text_news}"

        if link:
            text += f"\n\n🔗 {link}"

        if photo:
            await update.message.reply_photo(
                photo,
                caption=text,
                parse_mode="Markdown"
            )
        else:
            await update.message.reply_text(
                text,
                parse_mode="Markdown"
            )


# ───────────── ПРЕДПРОСМОТР ─────────────
async def show_preview(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message

    text = f"📰 Предпросмотр\n\n{context.user_data['title']}\n\n{context.user_data['text']}"

    if context.user_data.get("link"):
        text += f"\n\n🔗 {context.user_data['link']}"

    if context.user_data.get("photo"):
        await msg.reply_photo(
            context.user_data["photo"],
            caption=text,
            reply_markup=NEWS_ACTIONS_KB
        )
    else:
        await msg.reply_text(
            text,
            reply_markup=NEWS_ACTIONS_KB
        )


# ───────────── РАССЫЛКА ─────────────
async def broadcast_news(context: ContextTypes.DEFAULT_TYPE, item):
    subs = db_get_subscribers()

    title = item["title"]
    text_news = item["text"]
    photo = item["photo"]
    link = item["link"]

    text = f"{title}\n\n{text_news}"
    if link:
        text += f"\n{link}"

    for uid in subs:
        try:
            if photo:
                await context.bot.send_photo(uid, photo, caption=text)
            else:
                await context.bot.send_message(uid, text)
        except:
            pass


# ───────────── ГЛАВНЫЙ FLOW ─────────────
async def handle_news_flow(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message
    if not msg:
        return False

    text = msg.text or ""
    user_id = update.effective_user.id
    is_admin = user_id == ADMIN_CHAT_ID

    # ───── ПУБЛИКАЦИЯ ─────
    if text == "✅ Опубликовать":
        title = context.user_data.get("title")
        text_news = context.user_data.get("text")
        photo = context.user_data.get("photo")
        link = context.user_data.get("link")

        if not title or not text_news:
            await msg.reply_text("Ошибка публикации")
            return True

        db_add_news(title, text_news, photo, link)

        context.user_data.clear()
        await msg.reply_text(
            "✅ Новость опубликована",
            reply_markup=main_menu(is_admin)
        )
        return True

    # ───── ОТМЕНА ─────
    if text == "❌ Отмена":
        context.user_data.clear()
        await msg.reply_text(
            "❌ Добавление новости отменено",
            reply_markup=main_menu(is_admin)
        )
        return True

    # ───── АДМИН: РЕДАКТИРОВАТЬ ─────
    if text == "✏ Редактировать новость":
        news = db_get_news()
        if not news:
            await msg.reply_text("Новостей нет")
            return True

        for n in news:
            await msg.reply_text(f"{n['id']}. {n['title']}")

        context.user_data["admin_mode"] = "edit_select"
        return True

    # ───── АДМИН: УДАЛИТЬ ─────
    if text == "🗑 Удалить новость":
        news = db_get_news()
        if not news:
            await msg.reply_text("Новостей нет")
            return True

        for n in news:
            await msg.reply_text(f"{n['id']}. {n['title']}")

        context.user_data["admin_mode"] = "delete_select"
        return True

    # ───── АДМИН: РАССЫЛКА ─────
    if text == "📨 Разослать новость":
        news = db_get_news()
        if not news:
            await msg.reply_text("Новостей нет")
            return True

        for n in news:
            await msg.reply_text(f"{n['id']}. {n['title']}")

        context.user_data["admin_mode"] = "broadcast_select"
        return True

    # ───── ВЫБОР ID ─────
    if context.user_data.get("admin_mode"):
        try:
            nid = int(text)
        except:
            return True

        item = db_get_news_by_id(nid)
        if not item:
            await msg.reply_text("Новость не найдена")
            return True

        mode = context.user_data["admin_mode"]

        if mode == "delete_select":
            db_delete_news(nid)
            context.user_data.clear()
            await msg.reply_text(
                "🗑 Удалено",
                reply_markup=main_menu(is_admin)
            )
            return True

        if mode == "broadcast_select":
            await broadcast_news(context, item)
            context.user_data.clear()
            await msg.reply_text(
                "📨 Разослано",
                reply_markup=main_menu(is_admin)
            )
            return True

        if mode == "edit_select":
            context.user_data["edit_item"] = item
            context.user_data["admin_mode"] = "editing"
            await msg.reply_text(
                "Что редактировать?",
                reply_markup=NEWS_EDIT_KB
            )
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
