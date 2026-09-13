import base64
from email.mime.text import MIMEText
from pathlib import Path
from typing import cast

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ["https://www.googleapis.com/auth/gmail.send"]

BASE_DIR = Path(__file__).resolve().parents[3]
CREDENTIALS_FILE = BASE_DIR / "credentials.json"
TOKEN_FILE = BASE_DIR / "token.json"


def authenticate() -> Credentials:
    credentials = None

    if TOKEN_FILE.exists():
        credentials = Credentials.from_authorized_user_file(
            TOKEN_FILE,
            SCOPES,
        )

    if credentials is None or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                CREDENTIALS_FILE,
                SCOPES,
            )
            credentials = cast(
                Credentials,
                flow.run_local_server(port=0),
            )

        TOKEN_FILE.write_text(credentials.to_json())

    assert credentials is not None

    return credentials


def send_email(to: str | list, subject: str, body: str) -> None:
    credentials = authenticate()

    service = build(
        "gmail",
        "v1",
        credentials=credentials,
    )

    message = MIMEText(body, "html")
    message["to"] = ", ".join(to) if isinstance(to, list) else to
    message["subject"] = subject

    encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()

    service.users().messages().send(
        userId="me",
        body={"raw": encoded_message},
    ).execute()


if __name__ == "__main__":
    send_email(
        to="testemail",
        subject="Test",
        body="hello world",
    )
