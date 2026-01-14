import streamlit as st
from database.db import get_db
from biometric.capture_face import capture_face_image
from biometric.verify_face import verify_faces

def login():
    st.subheader("🔐 Login")

    username = st.text_input("Username")

    if st.button("Verify Face & Login"):
        if not username:
            st.error("Username required")
            return

        conn = get_db()
        c = conn.cursor()

        # STEP 2: fetch image path from DB
        c.execute(
            "SELECT face_image FROM users WHERE username=?",
            (username,)
        )
        row = c.fetchone()
        conn.close()

        if not row:
            st.error("User not found")
            return

        db_face_image = row[0]   # ✅ THIS IS A PATH (string)

        st.info("📷 Camera is on. Look straight.")
        live_face_path = capture_face_image()

        # STEP 4: verify using DeepFace
        if verify_faces(db_face_image, live_face_path):
            st.success("✅ Login successful")
            st.session_state.user = username
        else:
            st.error("❌ Face verification failed")



