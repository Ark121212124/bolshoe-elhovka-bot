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


# ─────────────────────────────
# 📢 ПОКАЗ НОВОСТЕЙ
# ─────────────────────────────
async def show_news(update: Update, context: ContextTypes.DEFAULT_TYPE):
    news = load_news()

    if not news:
        await update.message.reply_text("📰 *Новости поселения*\n\nПока новостей нет.", parse_mode="Markdown")
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
# 🧠 ОБРАБОТКА ШАГОВ НОВОСТЕЙ
# ─────────────────────────────
async def news_text_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    step = context.user_data.get("news_step")
    text = update.message.text if update.message else None

    if not step:
        return False

    # ─── ЗАГОЛОВОК ───
    if step == "title":
        context.user_data["news_title"] = text
        context.user_data["news_step"] = "text"
        await update.message.reply_text("📄 Введите *описание новости*:", parse_mode="Markdown")
        return True

    # ─── ОПИСАНИЕ ───
    if step == "text":
        context.user_data["news_text"] = text
        context.user_data["news_step"] = "photo"
        await update.message.reply_text("🖼 Отправьте *фото* или `-`", parse_mode="Markdown")
        return True

    # ─── ФОТО ───
    if step == "photo":
        if update.message.photo:
            context.user_data["news_photo"] = update.message.photo[-1].file_id
        else:
            context.user_data["news_photo"] = None

        context.user_data["news_step"] = "link"
        await update.message.reply_text("🔗 Введите *ссылку* или `-`", parse_mode="Markdown")
        return True

    # ─── ССЫЛКА + ПРЕДПРОСМОТР ───
    if step == "link":
        context.user_data["news_link"] = None if text == "-" else text
        context.user_data["news_step"] = "actions"

        await show_preview(update, context)
        return True

    # ─── ДЕЙСТВИЯ ───
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
        await update.message.reply_text("❌ Добавление новости отменено")
        return True

    if text == "✏ Редактировать":
        await update.message.reply_text("✏ *Что редактировать?*", parse_mode="Markdown", reply_markup=NEWS_EDIT_KB)
        return True

    # ─── РЕДАКТИРОВАНИЕ ───
    if text == "📝 Заголовок":
        context.user_data["news_step"] = "title"
        await update.message.reply_text("📝 Введите новый заголовок:")
        return True

    if text == "📄 Описание":
        context.user_data["news_step"] = "text"
        await update.message.reply_text("📄 Введите новое описание:")
        return True

    if text == "🖼 Фото":
        context.user_data["news_step"] = "photo"
        await update.message.reply_text("🖼 Отправьте новое фото или `-`")
        return True

    if text == "🔗 Ссылка":
        context.user_data["news_step"] = "link"
        await update.message.reply_text("🔗 Введите новую ссылку или `-`")
        return True

    return False


# ─────────────────────────────
# 👁 ПРЕДПРОСМОТР
# ─────────────────────────────
async def show_preview(update: Update, context: ContextTypes.DEFAULT_TYPE):
    preview = (
        f"📰 *Предпросмотр новости*\n\n"
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
