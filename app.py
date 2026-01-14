import streamlit as st

# ---------- DATABASE ----------
from database.db import create_table, get_db

# ---------- AUTH ----------
from auth.register import register
from biometric.verify_face import verify_faces
from biometric.capture_face import capture_face_image

# ---------- GMAIL ----------
from gmail.gmail_auth import get_service, get_gmail_token
from gmail.inbox import get_inbox

# ---------- VOICE ----------
from voice.speech_to_text import listen
from voice.text_to_speech import speak

# ======================================================
# ⚙️ INITIAL SETUP
# ======================================================
st.set_page_config(page_title="Voice Based Gmail", page_icon="🎤")
create_table()
st.title("🎤 Voice Based Gmail")

# ======================================================
# 🧠 SESSION
# ======================================================
if "user" not in st.session_state:
    st.session_state.user = None


# ======================================================
# 📌 SIDEBAR MENU
# ======================================================
menu = ["Register", "Login", "Inbox"]
choice = st.sidebar.selectbox("Menu", menu)


# ======================================================
# 🚪 LOGOUT (SIDEBAR)
# ======================================================
if st.session_state.user:
    if st.sidebar.button("🚪 Logout"):
        st.session_state.user = None
        st.success("Logged out successfully")
        st.rerun()


# ======================================================
# 📝 REGISTER
# ======================================================
if choice == "Register":
    st.subheader("📝 Register")

    username = st.text_input("Username")
    app_password = st.text_input("Google App Password", type="password")

    if st.button("Register"):
        if not username or not app_password:
            st.error("Please fill all fields")
        else:
            st.info("📷 Look at the camera")
            face_path = capture_face_image(filename=f"{username}.jpg")
            register(username, app_password, face_path)
            st.success("✅ Registration successful")


# ======================================================
# 🔐 LOGIN
# ======================================================
elif choice == "Login":
    st.subheader("🔐 Login")
    username = st.text_input("Username")

    if st.button("Verify Face & Login"):
        conn = get_db()
        c = conn.cursor()
        c.execute("SELECT face_image FROM users WHERE username=?", (username,))
        row = c.fetchone()

        if not row:
            st.error("❌ User not found")
            st.stop()

        live_face = capture_face_image(filename=f"live_{username}.jpg")

        if verify_faces(row[0], live_face):
            st.session_state.user = username
            st.success("✅ Login successful")
        else:
            st.error("❌ Face verification failed")


# ======================================================
# 📬 INBOX + VOICE ASSISTANT
# ======================================================
elif choice == "Inbox":

    if not st.session_state.user:
        st.error("❌ Please login first")
        st.stop()

    username = st.session_state.user
    conn = get_db()
    c = conn.cursor()

    c.execute("SELECT gmail_token FROM users WHERE username=?", (username,))
    token = c.fetchone()[0]

    if token is None:
        st.info("🔐 Gmail not connected")
        if st.button("Connect Gmail"):
            token = get_gmail_token()
            c.execute(
                "UPDATE users SET gmail_token=? WHERE username=?",
                (token, username)
            )
            conn.commit()
            st.success("✅ Gmail connected")
            st.rerun()
        st.stop()

    # ---------- LOAD INBOX ----------
    service = get_service(token)
    emails = get_inbox(service)

    # ==================================================
    # 📬 INBOX UI (SIMPLE LIST)
    # ==================================================
    st.subheader("📬 Inbox")

    for i, mail in enumerate(emails):
        st.markdown(f"**{i+1}.** {mail['snippet']}")

    # ==================================================
    # 🎙 VOICE ASSISTANT
    # ==================================================
    st.divider()
    st.subheader("🎙 Voice Assistant")

    status_box = st.empty()
    result_box = st.empty()

    def extract_number(text):
        words = {
            "one": 1, "two": 2, "three": 3,
            "four": 4, "five": 5
        }
        for w, n in words.items():
            if w in text:
                return n
        for t in text.split():
            if t.isdigit():
                return int(t)
        return None

    if st.button("🎤 Speak"):
        status_box.info("🎧 Listening...")

        try:
            command = listen().lower().strip()
            status_box.success("✅ Listening stopped")

            if not command:
                result_box.error("❌ Could not understand speech")
                speak("I could not understand you")
                st.stop()

            result_box.success(f"🗣 You said: **{command}**")

            # -------- LOGOUT BY VOICE --------
            if "logout" in command or "log out" in command:
                speak("Logging out")
                st.session_state.user = None
                st.success("Logged out successfully")
                st.rerun()

            # -------- READ EMAIL (SNIPPET ONLY) --------
            elif "read email" in command or "read mail" in command:
                num = extract_number(command)

                if not num or num > len(emails):
                    speak("Invalid email number")
                    st.error("Invalid email number")
                    st.stop()

                email_meta = emails[num - 1]

                speak(
                    f"Reading email {num}. "
                    f"{email_meta['snippet']}"
                )

            else:
                speak("Command not recognized")
                st.warning("Command not recognized")

        except Exception as e:
            status_box.error("❌ Voice command failed")
            st.error(str(e))
