import sqlite3
import os

DB_PATH = "storage/database.db"


def get_conn():
    return sqlite3.connect(DB_PATH)


# ───────────── ИНИЦИАЛИЗАЦИЯ ─────────────
def init_db():
    conn = get_conn()
    cur = conn.cursor()

    # Новости
    cur.execute("""
        CREATE TABLE IF NOT EXISTS news (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            text TEXT,
            photo TEXT,
            link TEXT,
            date TEXT
        )
    """)

    # Подписчики
    cur.execute("""
        CREATE TABLE IF NOT EXISTS subscribers (
            user_id INTEGER PRIMARY KEY
        )
    """)

    conn.commit()
    conn.close()


# ───────────── НОВОСТИ ─────────────
def db_add_news(title, text, photo, link, date):
    conn = get_conn()
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO news (title, text, photo, link, date) VALUES (?, ?, ?, ?, ?)",
        (title, text, photo, link, date)
    )

    conn.commit()
    conn.close()


def db_get_news():
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("SELECT * FROM news ORDER BY id DESC")
    rows = cur.fetchall()

    conn.close()

    result = []
    for r in rows:
        result.append({
            "id": r[0],
            "title": r[1],
            "text": r[2],
            "photo": r[3],
            "link": r[4],
            "date": r[5],
        })
    return result


def db_get_news_by_id(nid):
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("SELECT * FROM news WHERE id=?", (nid,))
    r = cur.fetchone()
    conn.close()

    if not r:
        return None

    return {
        "id": r[0],
        "title": r[1],
        "text": r[2],
        "photo": r[3],
        "link": r[4],
        "date": r[5],
    }


def db_delete_news(nid):
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("DELETE FROM news WHERE id=?", (nid,))
    conn.commit()
    conn.close()


# ───────────── ПОДПИСЧИКИ ─────────────
def db_add_subscriber(uid):
    conn = get_conn()
    cur = conn.cursor()

    cur.execute(
        "INSERT OR IGNORE INTO subscribers (user_id) VALUES (?)",
        (uid,)
    )

    conn.commit()
    conn.close()


def db_remove_subscriber(uid):
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("DELETE FROM subscribers WHERE user_id=?", (uid,))
    conn.commit()
    conn.close()


def db_get_subscribers():
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("SELECT user_id FROM subscribers")
    rows = cur.fetchall()
    conn.close()

    return [r[0] for r in rows]
