# # Import required libraries from Flask
# from flask import Flask, render_template, request, redirect, session, jsonify

# # Import database helper functions
# from database.db import create_table, get_db

# # Import authentication logic
# from auth.register import register
# from auth.login import login_user

# # Import face capture function
# from biometric.capture_face import capture_face_image

# # Import Gmail API functions
# from gmail.gmail_auth import get_service, get_gmail_token
# from gmail.inbox import get_inbox
# from gmail.send_mail import send_mail

# import re
# import base64

# app = Flask(__name__)

# app.secret_key = "voice-email-secret"

# # Create database table when app starts (if not exists)
# create_table()


# # ---------------- HOME PAGE ----------------------------
# @app.route("/")
# def home():
#     # If user already logged in, go to dashboard
#     if "user" in session:
#         return redirect("/dashboard")

#     # Otherwise show login page
#     return render_template("login.html")

# @app.route("/login", methods=["POST"])
# def login_route():
#     username = request.form["username"]
#     login_success, email = login_user(username)
#     if login_success:
#         session["user"] = email
#         return redirect("/platforms")   # NEW PAGE

# @app.route("/platforms")
# def platforms():
#     if "user" not in session:
#         return redirect("/login")
#     return render_template("platforms.html")


# # ---------------- REGISTER ------------------------
# @app.route("/register", methods=["GET", "POST"])
# def register_page():
#     if request.method == "POST":
#         # Get form data
#         username = request.form["username"]
#         email = request.form["email"]
#         password = request.form["password"]

#         # Capture user's face image using webcam
#         face_path = capture_face_image(filename=f"{username}.jpg")

#         # Save user details in database
#         register(username, email, password, face_path)

#         # Redirect to login page after registration
#         return redirect("/")

#     # Show registration page
#     return render_template("register.html")


# # ---------------- LOGIN WITH FACE ----------------
# @app.route("/login", methods=["POST"])
# def login():
#     username = request.form["username"]

#     # Verify face and login
#     if login_user(username):
#         session["user"] = username  # Store username in session
#         return redirect("/dashboard")

#     return "Face verification failed"

# @app.route("/whatsapp_dashboard")
# def whatsapp_dashboard():
#     if "user" not in session:
#         return redirect("/")
#     return render_template("whatsapp.html")

# from voice.speech_to_text import listen
# from voice.text_to_speech import speak

# @app.route("/platform_voice", methods=["POST"])
# def platform_voice():
#     command = listen()
#     if not command:
#         return jsonify({"status": "error"})

#     if "gmail" in command:
#         return jsonify({"redirect": "/dashboard"})

#     elif "whatsapp" in command:
#         return jsonify({"redirect": "/whatsapp_dashboard"})

#     return jsonify({"status": "unknown"})


# # ---------------- DASHBOARD (INBOX) -----------------------
# @app.route("/dashboard")
# def dashboard():
#     if "user" not in session:
#         return redirect("/")

#     username = session["user"]

#     # Get Gmail token from database
#     conn = get_db()
#     c = conn.cursor()
#     c.execute("SELECT gmail_token FROM users WHERE username=?", (username,))
#     row = c.fetchone()
#     conn.close()

#     token = row[0] if row else None

#     # If Gmail not connected yet, redirect to connect page
#     if token is None:
#         return redirect("/connect_gmail")

#     # Create Gmail API service
#     service = get_service(token)

#     # Fetch inbox emails
#     emails = get_inbox(service)

#     return render_template("dashboard.html", emails=emails)


# # ---------------- CONNECT GMAIL ----------------
# @app.route("/connect_gmail")
# def connect_gmail():
#     if "user" not in session:
#         return redirect("/")

#     # Get Gmail OAuth token
#     token = get_gmail_token()

#     # Save token in database
#     conn = get_db()
#     c = conn.cursor()
#     c.execute("UPDATE users SET gmail_token=? WHERE username=?", (token, session["user"]))
#     conn.commit()
#     conn.close()

#     return redirect("/dashboard")


# # ---------------- GET FULL EMAIL BODY ----------------
# def get_full_email(service, msg_id):
#     # Fetch full email data from Gmail
#     msg = service.users().messages().get(userId="me", id=msg_id, format="full").execute()

#     parts = msg["payload"].get("parts")
#     body = ""

#     # Decode email body
#     if parts:
#         for part in parts:
#             if part["mimeType"] == "text/plain":
#                 data = part["body"]["data"]
#                 body = base64.urlsafe_b64decode(data).decode("utf-8")
#                 break
#     else:
#         data = msg["payload"]["body"].get("data")
#         if data:
#             body = base64.urlsafe_b64decode(data).decode("utf-8")

#     return body[:2000]  # Return first 2000 characters


# # ---------------- VOICE COMMAND PROCESSING ----------------
# @app.route("/voice_command", methods=["POST"])
# def voice_command():
#     # Get spoken command from frontend
#     command = request.json.get("command", "").lower().strip()
#     print("🎙 Heard:", command)

#     # Convert spoken numbers into digits
#     word_to_num = {
#         "one": "1", "first": "1",
#         "two": "2", "second": "2",
#         "three": "3", "third": "3",
#         "four": "4", "fourth": "4",
#         "five": "5", "fifth": "5"
#     }

#     for word, num in word_to_num.items():
#         command = command.replace(word, num)

#     # Clean extra words that break pattern
#     command = command.replace("the ", "")
#     command = command.replace("my ", "")
#     command = command.replace("number ", "")
#     command = command.replace("email number", "email")

#     print("🧠 Cleaned Command:", command)

#     # Match "read email X"
#     match = re.search(r"read\s*email\s*(\d+)", command)

#     if match:
#         index = int(match.group(1)) - 1
#         print("📨 Email Index Requested:", index + 1)

#         # Get Gmail token
#         conn = get_db()
#         c = conn.cursor()
#         c.execute("SELECT gmail_token FROM users WHERE username=?", (session["user"],))
#         token = c.fetchone()[0]
#         conn.close()

#         service = get_service(token)
#         emails = get_inbox(service)

#         # If valid email number
#         if 0 <= index < len(emails):
#             email = emails[index]

#             sender = email.get("from", "Unknown sender")
#             subject = email.get("subject", "No subject")
#             snippet = email.get("snippet", "")

#             voice_summary = f"Email from {sender}. Subject: {subject}. Preview: {snippet}"
#             return jsonify(reply=voice_summary)

#         return jsonify(reply="That email number does not exist.")

#     return jsonify(reply="Sorry, I did not understand. Say read email 1")


# # ---------------- COMPOSE PAGE ----------------
# @app.route("/compose")
# def compose():
#     if "user" not in session:
#         return redirect("/")

#     # Get user's email address from database
#     conn = get_db()
#     c = conn.cursor()
#     c.execute("SELECT email FROM users WHERE username=?", (session["user"],))
#     row = c.fetchone()
#     conn.close()

#     user_email = row[0] if row else ""

#     return render_template("compose.html", user_email=user_email)


# # ---------------- SEND MAIL ----------------
# @app.route("/send_mail", methods=["POST"])
# def send_mail_route():
#     if "user" not in session:
#         return jsonify({"message": "Not logged in"})

#     data = request.json
#     to = data.get("to")
#     subject = data.get("subject")
#     message = data.get("message")

#     if not to or not subject or not message:
#         return jsonify({"message": "Missing email fields"})

#     # Get Gmail token
#     conn = get_db()
#     c = conn.cursor()
#     c.execute("SELECT gmail_token FROM users WHERE username=?", (session["user"],))
#     row = c.fetchone()
#     conn.close()

#     if not row or not row[0]:
#         return jsonify({"message": "Gmail not connected"})

#     token = row[0]
#     service = get_service(token)

#     try:
#         # Send email using Gmail API
#         send_mail(service, to, subject, message)
#         return jsonify({"message": "Email sent successfully ✅"})
#     except Exception as e:
#         print("SEND ERROR:", e)
#         return jsonify({"message": "Failed to send email"})


# # ---------------- SENT PAGE ----------------
# @app.route("/sent")
# def sent():
#     if "user" not in session:
#         return redirect("/")

#     # Get Gmail token
#     conn = get_db()
#     c = conn.cursor()
#     c.execute("SELECT gmail_token FROM users WHERE username=?", (session["user"],))
#     token = c.fetchone()[0]
#     conn.close()

#     service = get_service(token)

#     # Fetch sent emails instead of inbox
#     sent_mails = get_inbox(service, label="SENT")
#     return render_template("sent.html", emails=sent_mails, user=session["user"])


# # ---------------- LOGOUT ----------------
# @app.route("/logout")
# def logout():
#     session.clear()  # Clear session data
#     return redirect("/")


# # ---------------- RUN APP ----------------
# if __name__ == "__main__":
#     print("🚀 Starting Flask Server...")
#     app.run(debug=True, use_reloader=False)


from flask import Flask, render_template, request, redirect, session, jsonify
from database.db import create_table, get_db
from auth.register import register
from auth.login import login_user
from biometric.capture_face import capture_face_image

from gmail.gmail_auth import get_service, get_gmail_token
from gmail.inbox import get_inbox
from gmail.send_mail import send_mail

from voice.speech_to_text import listen
from voice.text_to_speech import speak

import re
import base64

app = Flask(__name__)
app.secret_key = "voice-email-secret"

create_table()

# ---------------- HOME ----------------
@app.route("/")
def home():
    if "user" in session:
        return redirect("/platforms")
    return render_template("login.html")


# ---------------- LOGIN ----------------
@app.route("/login", methods=["POST"])
def login_route():
    username = request.form["username"]

    login_success, email = login_user(username)
    if login_success:
        session["user"] = username  # store username consistently
        return redirect("/platforms")

    return "Login failed"


# ---------------- PLATFORMS PAGE ----------------
@app.route("/platforms")
def platforms():
    if "user" not in session:
        return redirect("/")
    return render_template("platforms.html")


# ---------------- REGISTER ----------------
@app.route("/register", methods=["GET", "POST"])
def register_page():
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]

        face_path = capture_face_image(filename=f"{username}.jpg")
        register(username, email, password, face_path)

        return redirect("/")

    return render_template("register.html")


# ---------------- WHATSAPP DASHBOARD ----------------
@app.route("/whatsapp_dashboard")
def whatsapp_dashboard():
    if "user" not in session:
        return redirect("/")
    return render_template("whatsapp.html")


# ---------------- VOICE PLATFORM SELECT ----------------
@app.route("/platform_voice", methods=["POST"])
def platform_voice():
    command = listen()
    if not command:
        return jsonify({"status": "error"})

    if "gmail" in command:
        return jsonify({"redirect": "/dashboard"})
    elif "whatsapp" in command:
        return jsonify({"redirect": "/whatsapp_dashboard"})

    return jsonify({"status": "unknown"})


# ---------------- GMAIL DASHBOARD ----------------
@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect("/")

    username = session["user"]

    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT gmail_token FROM users WHERE username=?", (username,))
    row = c.fetchone()
    conn.close()

    token = row[0] if row else None

    if token is None:
        return redirect("/connect_gmail")

    service = get_service(token)
    emails = get_inbox(service)

    return render_template("dashboard.html", emails=emails)


# ---------------- CONNECT GMAIL ----------------
@app.route("/connect_gmail")
def connect_gmail():
    if "user" not in session:
        return redirect("/")

    token = get_gmail_token()

    conn = get_db()
    c = conn.cursor()
    c.execute("UPDATE users SET gmail_token=? WHERE username=?", (token, session["user"]))
    conn.commit()
    conn.close()

    return redirect("/dashboard")


# ---------------- VOICE EMAIL READER ----------------
@app.route("/voice_command", methods=["POST"])
def voice_command():
    command = request.json.get("command", "").lower().strip()

    word_to_num = {
        "one": "1", "first": "1",
        "two": "2", "second": "2",
        "three": "3", "third": "3",
        "four": "4", "fourth": "4",
        "five": "5", "fifth": "5"
    }

    for word, num in word_to_num.items():
        command = command.replace(word, num)

    match = re.search(r"read\s*email\s*(\d+)", command)

    if match:
        index = int(match.group(1)) - 1

        conn = get_db()
        c = conn.cursor()
        c.execute("SELECT gmail_token FROM users WHERE username=?", (session["user"],))
        token = c.fetchone()[0]
        conn.close()

        service = get_service(token)
        emails = get_inbox(service)

        if 0 <= index < len(emails):
            email = emails[index]
            sender = email.get("from", "Unknown sender")
            subject = email.get("subject", "No subject")
            snippet = email.get("snippet", "")

            voice_summary = f"Email from {sender}. Subject: {subject}. Preview: {snippet}"
            return jsonify(reply=voice_summary)

        return jsonify(reply="That email number does not exist.")

    return jsonify(reply="Sorry, I did not understand. Say read email 1")


# ---------------- COMPOSE PAGE ----------------
@app.route("/compose")
def compose():
    if "user" not in session:
        return redirect("/")

    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT email FROM users WHERE username=?", (session["user"],))
    row = c.fetchone()
    conn.close()

    user_email = row[0] if row else ""
    return render_template("compose.html", user_email=user_email)


# ---------------- SEND MAIL ----------------
@app.route("/send_mail", methods=["POST"])
def send_mail_route():
    if "user" not in session:
        return jsonify({"message": "Not logged in"})

    data = request.json
    to = data.get("to")
    subject = data.get("subject")
    message = data.get("message")

    if not to or not subject or not message:
        return jsonify({"message": "Missing email fields"})

    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT gmail_token FROM users WHERE username=?", (session["user"],))
    row = c.fetchone()
    conn.close()

    if not row or not row[0]:
        return jsonify({"message": "Gmail not connected"})

    service = get_service(row[0])

    try:
        send_mail(service, to, subject, message)
        return jsonify({"message": "Email sent successfully ✅"})
    except Exception as e:
        print("SEND ERROR:", e)
        return jsonify({"message": "Failed to send email"})


# ---------------- SENT MAIL ----------------
@app.route("/sent")
def sent():
    if "user" not in session:
        return redirect("/")

    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT gmail_token FROM users WHERE username=?", (session["user"],))
    token = c.fetchone()[0]
    conn.close()

    service = get_service(token)
    sent_mails = get_inbox(service, label="SENT")

    return render_template("sent.html", emails=sent_mails)



from whatsapp_api import whatsapp_api



# ---------------- CONNECT WHATSAPP ----------------
@app.route("/connect_whatsapp")
def connect_whatsapp():
    if "user" not in session:
        return redirect("/")
    try:
        whatsapp_api.start_whatsapp(show_qr=True)
        return "<h2>WhatsApp Connected! You can close this tab.</h2>"
    except Exception as e:
        return f"<h2>Error connecting WhatsApp: {e}</h2>"

# ---------------- WHATSAPP AJAX ENDPOINTS ----------------
from flask import request

@app.route("/get_whatsapp_chats")
def get_whatsapp_chats():
    if "user" not in session:
        return jsonify({"error": "Not logged in"}), 401
    try:
        whatsapp_api.start_whatsapp(show_qr=False)
        chats = whatsapp_api.get_recent_chats()
        return jsonify({"chats": chats})
    except Exception as e:
        return jsonify({"error": str(e)})

@app.route("/get_whatsapp_messages")
def get_whatsapp_messages():
    if "user" not in session:
        return jsonify({"error": "Not logged in"}), 401
    contact_name = request.args.get("contact_name")
    try:
        whatsapp_api.start_whatsapp(show_qr=False)
        messages = whatsapp_api.get_messages(contact_name)
        return jsonify({"messages": messages})
    except Exception as e:
        return jsonify({"error": str(e)})

@app.route("/send_whatsapp_message", methods=["POST"])
def send_whatsapp_message():
    if "user" not in session:
        return jsonify({"error": "Not logged in"}), 401
    data = request.get_json()
    contact_name = data.get("contact_name")
    message = data.get("message")
    try:
        whatsapp_api.start_whatsapp(show_qr=False)
        ok = whatsapp_api.send_message(contact_name, message)
        return jsonify({"success": ok})
    except Exception as e:
        return jsonify({"error": str(e)})

@app.route("/forward_whatsapp_message", methods=["POST"])
def forward_whatsapp_message():
    if "user" not in session:
        return jsonify({"error": "Not logged in"}), 401
    data = request.get_json()
    to_contact = data.get("to_contact")
    message = data.get("message")
    try:
        whatsapp_api.start_whatsapp(show_qr=False)
        ok = whatsapp_api.forward_message(to_contact, message)
        return jsonify({"success": ok})
    except Exception as e:
        return jsonify({"error": str(e)})


@app.route("/webhook", methods=["GET", "POST"])
def whatsapp_webhook():
    if request.method == "GET":
        verify_token = "my_verify_token"
        if request.args.get("hub.verify_token") == verify_token:
            return request.args.get("hub.challenge")
        return "Verification failed"

    if request.method == "POST":
        data = request.json
        print("Incoming message:", data)
        # Save message to database here
        return "OK", 200


# ---------------- LOGOUT ----------------
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


# ---------------- RUN ----------------
if __name__ == "__main__":
    print("🚀 Starting Flask Server...")
    app.run(debug=True, use_reloader=False)



