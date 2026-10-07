import sqlite3

DATABASE = "leads.db"


def get_connection():
    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row
    return connection


def init_db():
    connection = get_connection()

    connection.execute("""
        CREATE TABLE IF NOT EXISTS leads (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            website TEXT UNIQUE,
            email TEXT,
            phone TEXT,
            source TEXT
        )
    """)

    connection.commit()
    connection.close()