import base64
from email.mime.text import MIMEText
import os
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from src.services.Gmail.scopes import SCOPES


def get_service():
    creds = None

    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'src/services/Gmail/credentials.json', SCOPES
            )
            creds = flow.run_local_server(port=8080, prompt='consent', access_type='offline')

        if creds:
            print("Credentials obtained successfully.")
            with open('token.json', 'w') as token:
                token.write(creds.to_json())
        else:
            print("Failed to obtain credentials.")
            return None

    service = build('gmail', 'v1', credentials=creds)
    return service

def create_message(sender, to, subject, message_text):
    message = MIMEText(message_text)
    message['to'] = to
    message['from'] = sender
    message['subject'] = subject

    raw_message = base64.urlsafe_b64encode(message.as_string().encode('utf-8'))
    return {'raw': raw_message.decode('utf-8')}

def send_message(service, user_id, message):
    try:
        sent_message = service.users().messages().send(userId=user_id, body=message).execute()
        print('Message Id:', sent_message['id'])
        return sent_message
    except Exception as e:
        print('An error occurred:', e)
        return None
    

def send_email_reply(to, subject, message_body, sender="pathakdeo24@gmail.com"):
    service = get_service()
    msg = create_message(sender, to, subject, message_body)
    return send_message(service, "me", msg)

