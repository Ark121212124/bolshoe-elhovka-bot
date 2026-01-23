import json
from telegram import Update
from telegram.ext import ContextTypes
from config import ADMIN_CHAT_ID

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


# ─────────────────────────
# 👥 ПРОСМОТР НОВОСТЕЙ
# ─────────────────────────
async def show_news(update: Update, context: ContextTypes.DEFAULT_TYPE):
    news = load_news()

    if not news:
        await update.message.reply_text("📰 *Новости поселения*\n\nПока новостей нет.", parse_mode="Markdown")
        return

    for item in reversed(news):
        text = f"*{item['title']}*\n\n{item['text']}"
        if item.get("link"):
            text += f"\n\n🔗 {item['link']}"

        if item.get("photo"):
            await update.message.reply_photo(item["photo"], caption=text, parse_mode="Markdown")
        else:
            await update.message.reply_text(text, parse_mode="Markdown")


# ─────────────────────────
# 🛠 ДОБАВЛЕНИЕ НОВОСТИ (АДМИН)
# ─────────────────────────
async def news_text_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_CHAT_ID:
        return False

    step = context.user_data.get("news_step")
    if not step:
        return False

    text = update.message.text

    if step == "title":
        context.user_data["news_title"] = text
        context.user_data["news_step"] = "text"
        await update.message.reply_text("📝 Введите *описание новости*:", parse_mode="Markdown")
        return True

    if step == "text":
        context.user_data["news_text"] = text
        context.user_data["news_step"] = "photo"
        await update.message.reply_text("🖼 Отправьте фото или напишите `-` чтобы пропустить")
        return True

    if step == "photo":
        if text != "-":
            await update.message.reply_text("⚠ Отправьте *фото*, либо `-`")
            return True

        context.user_data["news_photo"] = None
        context.user_data["news_step"] = "link"
        await update.message.reply_text("🔗 Введите ссылку или `-`")
        return True

    if step == "link":
        context.user_data["news_link"] = None if text == "-" else text

        # предпросмотр
        title = context.user_data["news_title"]
        body = context.user_data["news_text"]
        link = context.user_data["news_link"]

        preview = f"*{title}*\n\n{body}"
        if link:
            preview += f"\n\n🔗 {link}"

        await update.message.reply_text(
            preview + "\n\n✅ Напишите `опубликовать` или `отмена`",
            parse_mode="Markdown"
        )

        context.user_data["news_step"] = "confirm"
        return True

    if step == "confirm":
        if text.lower() == "отмена":
            context.user_data.clear()
            await update.message.reply_text("❌ Добавление новости отменено")
            return True

        if text.lower() == "опубликовать":
            news = load_news()
            news.append({
                "title": context.user_data["news_title"],
                "text": context.user_data["news_text"],
                "photo": context.user_data.get("news_photo"),
                "link": context.user_data.get("news_link"),
            })
            save_news(news)

            await update.message.reply_text("✅ Новость опубликована")

            # рассылка подписчикам
            try:
                from handlers.subscriptions import load as load_subs
                subs = load_subs()
                for uid in subs:
                    try:
                        await context.bot.send_message(uid, f"📰 *Новая новость!*\n\n{context.user_data['news_title']}", parse_mode="Markdown")
                    except:
                        pass
            except:
                pass

            context.user_data.clear()
            return True

    return False


# ─────────────────────────
# 🖼 ФОТО ДЛЯ НОВОСТИ
# ─────────────────────────
async def news_photo_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.user_data.get("news_step") == "photo":
        photo = update.message.photo[-1].file_id
        context.user_data["news_photo"] = photo
        context.user_data["news_step"] = "link"
        await update.message.reply_text("🔗 Введите ссылку или `-`")
        return True
    return False
