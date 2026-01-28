from email.mime.text import MIMEText
import base64

def send_mail(service, to, subject, message_text):
    message = MIMEText(message_text)
    message["to"] = to
    message["subject"] = subject

    raw = base64.urlsafe_b64encode(message.as_bytes()).decode()

    body = {"raw": raw}
    service.users().messages().send(userId="me", body=body).execute()

