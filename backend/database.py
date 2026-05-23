import sqlite3
from pathlib import Path

APP_DIR = (
    Path.home()
    / ".local"
    / "share"
    / "credential-manager"
)

APP_DIR.mkdir(
    parents=True,
    exist_ok=True
)

DB_PATH = APP_DIR / "credentials.db"


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    return conn


def create_table():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS credentials (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            website TEXT UNIQUE NOT NULL,
            username TEXT NOT NULL,
            password TEXT,
            metadata TEXT
        )
    """)

    conn.commit()
    conn.close()