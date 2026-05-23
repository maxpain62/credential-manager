import sqlite3
from pathlib import Path

DB_PATH = Path("data/credentials.db")


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