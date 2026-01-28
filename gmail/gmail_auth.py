import pickle
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = [
    "https://www.googleapis.com/auth/gmail.readonly",
    "https://www.googleapis.com/auth/gmail.send"
]
def get_gmail_token():
    flow = InstalledAppFlow.from_client_secrets_file(
        "client_secret.json",
        SCOPES
    )
    creds = flow.run_local_server(port=0)
    return pickle.dumps(creds)

def get_service(token):
    creds = pickle.loads(token)
    return build("gmail", "v1", credentials=creds)
