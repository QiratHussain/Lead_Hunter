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


def save_leads(leads):
    connection = get_connection()

    for lead in leads:
        try:
            connection.execute(
                """
                INSERT INTO leads
                (name, website, email, phone, source)
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    lead["name"],
                    lead["website"],
                    lead["email"],
                    lead["phone"],
                    lead["source"],
                ),
            )
        except sqlite3.IntegrityError:
            # The website is already in the database.
            pass

    connection.commit()
    connection.close()


def get_leads():
    connection = get_connection()

    leads = connection.execute(
        "SELECT * FROM leads ORDER BY id DESC"
    ).fetchall()

    connection.close()

    return leads
