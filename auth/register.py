# import streamlit as st
# import pickle
# import hashlib
# from database.db import get_db
# from biometric.capture_face import capture_face

# def hash_password(password):
#     return hashlib.sha256(password.encode()).hexdigest()

# def register():
#     st.header("📝 Register")

#     username = st.text_input("Username")
#     app_password = st.text_input(
#         "Google App Password",
#         type="password",
#         help="Use Google App Password (16 characters)"
#     )

#     if st.button("Register"):
#         if not username or not app_password:
#             st.error("All fields are required")
#             return

#         try:
#             face_encoding = capture_face()

#             conn = get_db()
#             c = conn.cursor()
#             c.execute(
#                 "INSERT INTO users (username, app_password, face_encoding) VALUES (?, ?, ?)",
#                 (
#                     username,
#                     hash_password(app_password),
#                     pickle.dumps(face_encoding)
#                 )
#             )
#             conn.commit()

#             st.success("✅ Registration successful")

#         except ValueError as e:
#             st.error(str(e))
#         except Exception as e:
#             st.error("Registration failed")
#             st.exception(e)

import sqlite3
import pickle

DB_PATH = "database/users.db"

def register(username, app_password, face_image_path):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("""
        INSERT INTO users (username, app_password, face_image)
        VALUES (?, ?, ?)
    """, (username, app_password, face_image_path))

    conn.commit()
    conn.close()
