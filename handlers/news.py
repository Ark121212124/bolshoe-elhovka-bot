from telegram import Update
from telegram.ext import ContextTypes

from keyboards.news import NEWS_ACTIONS_KB, NEWS_EDIT_KB
from keyboards.main import main_menu
from config import ADMIN_CHAT_ID


# ───────── ХРАНИЛИЩЕ В ПАМЯТИ ─────────
NEWS_STORAGE = []   # список новостей
NEWS_ID = 1          # авто-id


# ───────── ПОКАЗ НОВОСТЕЙ ─────────
async def show_news(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message
    if not msg:
        return

    if not NEWS_STORAGE:
        await msg.reply_text("📰 Пока новостей нет.")
        return

    for n in reversed(NEWS_STORAGE):
        text = f"*{n['title']}*\n\n{n['text']}"

        if n["link"]:
            text += f"\n\n🔗 {n['link']}"

        if n["photo"]:
            await msg.reply_photo(
                n["photo"],
                caption=text,
                parse_mode="Markdown"
            )
        else:
            await msg.reply_text(
                text,
                parse_mode="Markdown"
            )


# ───────── ПРЕДПРОСМОТР ─────────
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


# ───────── ГЛАВНЫЙ FLOW ─────────
async def handle_news_flow(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global NEWS_ID

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

        NEWS_STORAGE.append({
            "id": NEWS_ID,
            "title": title,
            "text": text_news,
            "photo": photo,
            "link": link
        })

        NEWS_ID += 1

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
            "❌ Отменено",
            reply_markup=main_menu(is_admin)
        )
        return True

    # ───── АДМИН: УДАЛИТЬ ─────
    if text == "🗑 Удалить новость" and is_admin:
        if not NEWS_STORAGE:
            await msg.reply_text("Новостей нет")
            return True

        for n in NEWS_STORAGE:
            await msg.reply_text(f"{n['id']}. {n['title']}")

        context.user_data["admin_mode"] = "delete"
        return True

    # ───── ВЫБОР ID ─────
    if context.user_data.get("admin_mode") == "delete":
        try:
            nid = int(text)
        except:
            return True

        for n in NEWS_STORAGE:
            if n["id"] == nid:
                NEWS_STORAGE.remove(n)
                context.user_data.clear()
                await msg.reply_text(
                    "🗑 Удалено",
                    reply_markup=main_menu(is_admin)
                )
                return True

        await msg.reply_text("Новость не найдена")
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
