import requests
import sys
import getopt


# send slack message using API

def send_slack_message(message: str):
   
    webhook_url = 'https://hooks.slack.com/services/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'
    
    payload = {
        "text": message
    }

    response = requests.post(webhook_url, json=payload, headers={'Content-Type': 'application/json'})

    if response.status_code != 200:
        raise Exception(f"Request to Slack returned error: {response.status_code}, response: {response.text}")
