from flask import Flask, jsonify, send_file
import psycopg2
import pandas as pd
from io import BytesIO
from src.services.Gmail.get_emails import getEmails
from src.services.Gmail.send_email import send_email_reply
from flask import request
from src.services.Slack.slackMessage import send_slack_message


app = Flask(__name__)

def fetch_emails_from_db():
    conn = psycopg2.connect(
            dbname="emailDB",
            user="postgres",
            password="123456789",
            host="localhost",
            # port="5432"
    )

    df = pd.read_sql("SELECT * FROM emails ORDER BY timestamp DESC", conn)
    conn.close()
    return df

@app.route('/emails',methods=['GET'])
def get_emails():
    df = fetch_emails_from_db()
    csv_buffer = BytesIO()
    df.to_csv(csv_buffer, index=False)
    csv_buffer.seek(0)
    return send_file(csv_buffer, mimetype='text/csv', as_attachment=True, download_name='emails.csv')

@app.route('/send_email', methods=['POST'])
def send_email():
    data = request.get_json()
    to = data.get('to')
    subject = data.get('subject')
    message_body = data.get('message')
    
    if not to or not subject or not message_body:
        return jsonify({"error": "Missing required fields"}), 400
    
    try:
        send_email_reply(to, subject, message_body)
        return jsonify({"message": "Email sent successfully!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/send_slack_message', methods=['POST'])
def slack_notify():
    data = request.get_json()
    message = data.get('message')

    if not message:
        return jsonify({"error": "Missing 'message' field"}), 400

    try:
        send_slack_message(message)
        return jsonify({"message": "Slack message sent successfully!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    

if __name__ == '__main__':
    print("Fetching emails from Gmail...")
    getEmails()
    print("Emails fetched successfully!")
    print("Starting Flask server...")
    app.run(debug=True, port=5000)
