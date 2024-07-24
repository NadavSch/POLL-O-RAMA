import requests
import json

API_BASE_URL = "http://hackathons.masterschool.com:3030"
TEAM_NAME = "CTRL_ALT_DEFEAT"
PHONE_NUMBER = "4917670509437"

def register_team():
    url = f"{API_BASE_URL}/team/registerNumber"
    data = {
        "teamName": TEAM_NAME,
        "phoneNumber": PHONE_NUMBER
    }
    print(f"Sending request to {url} with data: {json.dumps(data, indent=4)}")
    response = requests.post(url, json=data)
    if response.status_code == 200:
        print("Team registered successfully")
    else:
        print(f"Failed to register team: {response.status_code} - {response.text}")

def send_sms():
    url = f"{API_BASE_URL}/sms/send"
    data = {
        "phoneNumber": PHONE_NUMBER,
        "message": "SUBSCRIBE CTRL_ALT_DEFEAT",
        "sender": TEAM_NAME
    }
    print(f"Sending request to {url} with data: {json.dumps(data, indent=4)}")
    response = requests.post(url, json=data)
    if response.status_code == 200:
        print("SMS sent successfully")
    else:
        print(f"Failed to send SMS: {response.status_code} - {response.text}")

def get_messages():
    url = f"{API_BASE_URL}/team/getMessages/{TEAM_NAME}"
    print(f"Sending request to {url}")
    response = requests.get(url)
    if response.status_code == 200:
        messages = response.json()
        print("Retrieved messages:", json.dumps(messages, indent=4))
    else:
        print(f"Failed to retrieve messages: {response.status_code} - {response.text}")

if __name__ == "__main__":
    register_team()
    send_sms()
    get_messages()