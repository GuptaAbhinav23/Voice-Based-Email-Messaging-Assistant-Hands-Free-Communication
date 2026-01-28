import base64

def get_full_email(service, msg_id):
    message = service.users().messages().get(userId='me', id=msg_id, format='full').execute()

    parts = message['payload'].get('parts', [])
    body = ""

    def extract_text(parts):
        text = ""
        for part in parts:
            mime = part.get("mimeType", "")
            if mime == "text/plain":
                data = part['body'].get('data')
                if data:
                    text += base64.urlsafe_b64decode(data).decode(errors="ignore")
            elif 'parts' in part:
                text += extract_text(part['parts'])
        return text

    body = extract_text(parts)

    if not body:
        body = "Sorry, I could not read the email body."

    return body[:2000]  # limit for TTS
