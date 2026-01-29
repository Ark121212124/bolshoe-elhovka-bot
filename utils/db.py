import sqlite3
from pathlib import Path

DB_PATH = "storage/bot.db"


def get_conn():
    Path("storage").mkdir(exist_ok=True)
    return sqlite3.connect(DB_PATH)


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
            id INTEGER PRIMARY KEY
        )
    """)

    conn.commit()
    conn.close()
