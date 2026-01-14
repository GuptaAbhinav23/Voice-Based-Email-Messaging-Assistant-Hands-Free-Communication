def get_inbox(service, max_results=5):
    results = service.users().messages().list(
        userId="me",
        labelIds=["INBOX"],
        maxResults=max_results
    ).execute()

    messages = results.get("messages", [])
    inbox = []

    for msg in messages:
        msg_data = service.users().messages().get(
            userId="me",
            id=msg["id"],
            format="metadata"   # 🔥 FAST
        ).execute()

        headers = msg_data["payload"]["headers"]

        subject = ""
        sender = ""

        for h in headers:
            if h["name"] == "Subject":
                subject = h["value"]
            if h["name"] == "From":
                sender = h["value"]

        inbox.append({
            "id": msg["id"],
            "from": sender,
            "subject": subject,
            "snippet": msg_data.get("snippet", "")
        })

    return inbox






