# gmail_utils.py

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from src.services.Gmail.scopes import SCOPES

import os.path
import base64
from bs4 import BeautifulSoup
import psycopg2


def getEmails():
    creds = None

    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('src/services/Gmail/credentials.json', SCOPES)
            creds = flow.run_local_server(port=8080, prompt='consent', access_type='offline')

        if creds:
            print("Credentials obtained successfully.")
            with open('token.json', 'w') as token:
                token.write(creds.to_json())
        else:
            print("Failed to obtain credentials.")
            return

    service = build('gmail', 'v1', credentials=creds)
    result = service.users().messages().list(userId='me').execute()

    if 'messages' not in result:
        print("No emails found.")
        return

    messages = result.get('messages')
    print(f"Found {len(messages)} emails.")

    try:
        conn = psycopg2.connect(
            dbname="emailDB",
            user="postgres",
            password="123456789",
            host="localhost",
            port="5432"
        )
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS emails (
                id SERIAL PRIMARY KEY,
                message_id TEXT UNIQUE,
                subject TEXT,
                sender TEXT,
                body TEXT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        conn.commit()

    except Exception as db_error:
        print(f"Database connection error: {db_error}")
        return

    for msg in messages:
        txt = service.users().messages().get(userId='me', id=msg['id']).execute()

        try:
            payload = txt['payload']
            headers = payload['headers']

            subject = sender = "No Subject"
            for d in headers:
                if d['name'] == 'Subject':
                    subject = d['value']
                if d['name'] == 'From':
                    sender = d['value']

            data = None
            if 'body' in payload and 'data' in payload['body']:
                data = payload['body']['data']
            elif 'parts' in payload:
                for part in payload['parts']:
                    if part['mimeType'] == 'text/plain':
                        data = part['body'].get('data')
                        break

            if not data:
                print(f"Skipping email with ID: {msg['id']} (No body found)")
                continue

            data = data.replace("-", "+").replace("_", "/")
            decoded_data = base64.b64decode(data).decode("utf-8", errors="ignore")

            soup = BeautifulSoup(decoded_data, "lxml")
            body = soup.get_text(strip=True)

            try:
                cursor.execute("""
                    INSERT INTO emails (message_id, subject, sender, body)
                    VALUES (%s, %s, %s, %s)
                    ON CONFLICT (message_id) DO NOTHING;
                """, (msg['id'], subject, sender, body))
                conn.commit()
                print(f"Saved email '{subject}' to database.")
            except Exception as db_err:
                print(f"Database error for message {msg['id']}: {db_err}")

        except Exception as e:
            print(f"Error processing email {msg['id']}: {str(e)}")

    cursor.close()
    conn.close()
    print("Database connection closed.")
