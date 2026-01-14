import sqlite3

def get_db():
    return sqlite3.connect("database/users.db")

def create_table():
    conn = get_db()
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            app_password TEXT,
            face_image TEXT,
            gmail_token BLOB
        )
    """)

    conn.commit()
    conn.close()
