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
