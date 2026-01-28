# Import required libraries from Flask
from flask import Flask, render_template, request, redirect, session, jsonify

# Import database helper functions
from database.db import create_table, get_db

# Import authentication logic
from auth.register import register
from auth.login import login_user

# Import face capture function
from biometric.capture_face import capture_face_image

# Import Gmail API functions
from gmail.gmail_auth import get_service, get_gmail_token
from gmail.inbox import get_inbox
from gmail.send_mail import send_mail

import re
import base64

# Create Flask app instance
app = Flask(__name__)

# Secret key used to manage sessions securely
app.secret_key = "voice-email-secret"

# Create database table when app starts (if not exists)
create_table()


# ---------------- HOME PAGE ----------------------------
@app.route("/")
def home():
    # If user already logged in, go to dashboard
    if "user" in session:
        return redirect("/dashboard")

    # Otherwise show login page
    return render_template("login.html")


# ---------------- REGISTER ------------------------
@app.route("/register", methods=["GET", "POST"])
def register_page():
    if request.method == "POST":
        # Get form data
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]

        # Capture user's face image using webcam
        face_path = capture_face_image(filename=f"{username}.jpg")

        # Save user details in database
        register(username, email, password, face_path)

        # Redirect to login page after registration
        return redirect("/")

    # Show registration page
    return render_template("register.html")


# ---------------- LOGIN WITH FACE ----------------
@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]

    # Verify face and login
    if login_user(username):
        session["user"] = username  # Store username in session
        return redirect("/dashboard")

    return "Face verification failed"


# ---------------- DASHBOARD (INBOX) -----------------------
@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect("/")

    username = session["user"]

    # Get Gmail token from database
    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT gmail_token FROM users WHERE username=?", (username,))
    row = c.fetchone()
    conn.close()

    token = row[0] if row else None

    # If Gmail not connected yet, redirect to connect page
    if token is None:
        return redirect("/connect_gmail")

    # Create Gmail API service
    service = get_service(token)

    # Fetch inbox emails
    emails = get_inbox(service)

    return render_template("dashboard.html", emails=emails)


# ---------------- CONNECT GMAIL ----------------
@app.route("/connect_gmail")
def connect_gmail():
    if "user" not in session:
        return redirect("/")

    # Get Gmail OAuth token
    token = get_gmail_token()

    # Save token in database
    conn = get_db()
    c = conn.cursor()
    c.execute("UPDATE users SET gmail_token=? WHERE username=?", (token, session["user"]))
    conn.commit()
    conn.close()

    return redirect("/dashboard")


# ---------------- GET FULL EMAIL BODY ----------------
def get_full_email(service, msg_id):
    # Fetch full email data from Gmail
    msg = service.users().messages().get(userId="me", id=msg_id, format="full").execute()

    parts = msg["payload"].get("parts")
    body = ""

    # Decode email body
    if parts:
        for part in parts:
            if part["mimeType"] == "text/plain":
                data = part["body"]["data"]
                body = base64.urlsafe_b64decode(data).decode("utf-8")
                break
    else:
        data = msg["payload"]["body"].get("data")
        if data:
            body = base64.urlsafe_b64decode(data).decode("utf-8")

    return body[:2000]  # Return first 2000 characters


# ---------------- VOICE COMMAND PROCESSING ----------------
@app.route("/voice_command", methods=["POST"])
def voice_command():
    # Get spoken command from frontend
    command = request.json.get("command", "").lower().strip()
    print("🎙 Heard:", command)

    # Convert spoken numbers into digits
    word_to_num = {
        "one": "1", "first": "1",
        "two": "2", "second": "2",
        "three": "3", "third": "3",
        "four": "4", "fourth": "4",
        "five": "5", "fifth": "5"
    }

    for word, num in word_to_num.items():
        command = command.replace(word, num)

    # Clean extra words that break pattern
    command = command.replace("the ", "")
    command = command.replace("my ", "")
    command = command.replace("number ", "")
    command = command.replace("email number", "email")

    print("🧠 Cleaned Command:", command)

    # Match "read email X"
    match = re.search(r"read\s*email\s*(\d+)", command)

    if match:
        index = int(match.group(1)) - 1
        print("📨 Email Index Requested:", index + 1)

        # Get Gmail token
        conn = get_db()
        c = conn.cursor()
        c.execute("SELECT gmail_token FROM users WHERE username=?", (session["user"],))
        token = c.fetchone()[0]
        conn.close()

        service = get_service(token)
        emails = get_inbox(service)

        # If valid email number
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

    # Get user's email address from database
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

    # Get Gmail token
    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT gmail_token FROM users WHERE username=?", (session["user"],))
    row = c.fetchone()
    conn.close()

    if not row or not row[0]:
        return jsonify({"message": "Gmail not connected"})

    token = row[0]
    service = get_service(token)

    try:
        # Send email using Gmail API
        send_mail(service, to, subject, message)
        return jsonify({"message": "Email sent successfully ✅"})
    except Exception as e:
        print("SEND ERROR:", e)
        return jsonify({"message": "Failed to send email"})


# ---------------- SENT PAGE ----------------
@app.route("/sent")
def sent():
    if "user" not in session:
        return redirect("/")

    # Get Gmail token
    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT gmail_token FROM users WHERE username=?", (session["user"],))
    token = c.fetchone()[0]
    conn.close()

    service = get_service(token)

    # Fetch sent emails instead of inbox
    sent_mails = get_inbox(service, label="SENT")
    return render_template("sent.html", emails=sent_mails, user=session["user"])


# ---------------- LOGOUT ----------------
@app.route("/logout")
def logout():
    session.clear()  # Clear session data
    return redirect("/")


# ---------------- RUN APP ----------------
if __name__ == "__main__":
    print("🚀 Starting Flask Server...")
    app.run(debug=True, use_reloader=False)
