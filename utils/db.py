import os
import psycopg2
from datetime import datetime

DB_URL = os.getenv("DATABASE_URL")


def get_conn():
    return psycopg2.connect(DB_URL)


def init_db():
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS news (
            id SERIAL PRIMARY KEY,
            title TEXT,
            text TEXT,
            photo TEXT,
            link TEXT,
            date TEXT
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS subscribers (
            user_id BIGINT PRIMARY KEY
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
        VALUES (%s, %s, %s, %s, %s)
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

    cur.execute("SELECT * FROM news WHERE id=%s", (nid,))
    row = cur.fetchone()
    conn.close()

    return row


def db_delete_news(nid):
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("DELETE FROM news WHERE id=%s", (nid,))
    conn.commit()
    conn.close()


def db_update_news(nid, field, value):
    conn = get_conn()
    cur = conn.cursor()

    cur.execute(f"UPDATE news SET {field}=%s WHERE id=%s", (value, nid))
    conn.commit()
    conn.close()


# ───────── ПОДПИСЧИКИ ─────────

def db_add_sub(user_id):
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("INSERT INTO subscribers VALUES (%s) ON CONFLICT DO NOTHING", (user_id,))
    conn.commit()
    conn.close()


def db_remove_sub(user_id):
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("DELETE FROM subscribers WHERE user_id=%s", (user_id,))
    conn.commit()
    conn.close()


def db_get_subscribers():
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("SELECT user_id FROM subscribers")
    rows = cur.fetchall()
    conn.close()

    return [r[0] for r in rows]
