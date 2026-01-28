def get_inbox(service, label="INBOX"):
    # Map friendly name to Gmail label ID
    label_map = {
        "INBOX": "INBOX",
        "SENT": "SENT"
    }

    label_id = label_map.get(label.upper(), "INBOX")

    results = service.users().messages().list(
        userId='me',
        labelIds=[label_id],
        maxResults=10
    ).execute()

    messages = results.get('messages', [])
    emails = []

    for msg in messages:
        msg_data = service.users().messages().get(userId='me', id=msg['id']).execute()
        headers = msg_data['payload']['headers']

        email = {
            "id": msg['id'],
            "from": "",
            "to": "",
            "subject": "",
            "snippet": msg_data.get("snippet", "")
        }

        for h in headers:
            if h['name'] == 'From':
                email['from'] = h['value']
            if h['name'] == 'To':
                email['to'] = h['value']
            if h['name'] == 'Subject':
                email['subject'] = h['value']

        emails.append(email)

    return emails






