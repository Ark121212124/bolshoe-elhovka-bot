import json
from telegram import Update
from telegram.ext import ContextTypes
from keyboards.subscriptions import SUB_KB

FILE = "storage/subscribers.json"


def load():
    try:
        with open(FILE, "r") as f:
            return json.load(f)
    except:
        return []


def save(data):
    with open(FILE, "w") as f:
        json.dump(data, f)


async def subscriptions_callbacks(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    subs = load()
    uid = query.from_user.id

    if query.data == "sub_on":
        if uid not in subs:
            subs.append(uid)
            save(subs)
        text = "🔔 Вы подписались на новости"

    elif query.data == "sub_off":
        if uid in subs:
            subs.remove(uid)
            save(subs)
        text = "🔕 Вы отписались от новостей"

    else:
        text = "🔔 Управление подпиской"

    await query.message.edit_text(
        text,
        reply_markup=SUB_KB
    )
