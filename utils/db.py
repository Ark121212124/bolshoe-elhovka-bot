import sqlite3
import os
from datetime import datetime

DB_PATH = "bot.db"


def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_conn()
    cur = conn.cursor()

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

    cur.execute("""
        CREATE TABLE IF NOT EXISTS subscribers (
            user_id INTEGER PRIMARY KEY
        )
    """)

    conn.commit()
    conn.close()


# ───────── НОВОСТИ ─────────

def db_add_news(title, text, photo=None, link=None):
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO news (title, text, photo, link, date)
        VALUES (?, ?, ?, ?, ?)
    """, (title, text, photo, link, datetime.now().strftime("%Y-%m-%d")))

    conn.commit()
    conn.close()


def db_get_news():
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("SELECT * FROM news ORDER BY id DESC")
    rows = cur.fetchall()
    conn.close()

    return rows


def db_get_news_by_id(nid):
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("SELECT * FROM news WHERE id = ?", (nid,))
    row = cur.fetchone()
    conn.close()

    return row


def db_delete_news(nid):
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("DELETE FROM news WHERE id = ?", (nid,))
    conn.commit()
    conn.close()


def db_update_news(nid, field, value):
    conn = get_conn()
    cur = conn.cursor()

    query = f"UPDATE news SET {field} = ? WHERE id = ?"
    cur.execute(query, (value, nid))

    conn.commit()
    conn.close()


# ───────── ПОДПИСЧИКИ ─────────

def db_add_sub(user_id):
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("INSERT OR IGNORE INTO subscribers VALUES (?)", (user_id,))
    conn.commit()
    conn.close()


def db_get_subscribers():
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("SELECT user_id FROM subscribers")
    rows = cur.fetchall()
    conn.close()

    return [r[0] for r in rows]
