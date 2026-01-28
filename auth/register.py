import sqlite3
import pickle

DB_PATH = "database/users.db"

def register(username, email, password, face_path):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("""
        INSERT INTO users (username, email, password, face_path)
        VALUES (?, ?, ?, ?)
    """, (username, email, password, face_path))

    conn.commit()
    conn.close()
