import requests
import time

API_BASE_URL = "http://hackathons.masterschool.com:3030"
TEAM_NAME = "CTRL_ALT_DEFEAT"
HACKATHON_NUMBER = "491771786208"
TEST_USER_NUMBER = "4917663346054"  # Your test user number


def send_sms(phone_number, message):
    endpoint = f"{API_BASE_URL}/sms/send"
    data = {"phoneNumber": phone_number, "message": message, "sender": TEAM_NAME}
    try:
        response = requests.post(endpoint, json=data)
        print(f"Send SMS response: {response.status_code}")
        print(f"Response content: {response.text}")
        return response.status_code == 200
    except requests.exceptions.RequestException as e:
        print(f"An error occurred while sending SMS: {e}")
        return False


def get_messages():
    endpoint = f"{API_BASE_URL}/team/getMessages/{TEAM_NAME}"
    try:
        response = requests.get(endpoint)
        print(f"Get messages response: {response.status_code}")
        print(f"Response content: {response.text}")
        if response.status_code == 200:
            messages = response.json()
            print(f"Received {len(messages)} message groups:")
            for sender, message_list in messages[0].items():
                for msg in message_list:
                    print(f"From: {sender}, Message: {msg['text']}, Received at: {msg['receivedAt']}")
            return messages
        else:
            print("Failed to retrieve messages")
            return []
    except requests.exceptions.RequestException as e:
        print(f"An error occurred while getting messages: {e}")
        return []


# Test the flow
print(f"Step 1: Sending instructions to the user's number ({TEST_USER_NUMBER})...")
instruction_message = f"To subscribe, please send 'SUBSCRIBE {TEAM_NAME}' to {HACKATHON_NUMBER}"
if send_sms(TEST_USER_NUMBER, instruction_message):
    print("\nInstructions sent successfully to the user.")
    print(f"The user should now send 'SUBSCRIBE {TEAM_NAME}' to the hackathon number ({HACKATHON_NUMBER}).")
    print("\nWaiting for 60 seconds to allow time for the user to send the subscription message...")
    time.sleep(60)

    print("\nStep 2: Checking for messages...")
    messages = get_messages()

    # Check if we received any messages
    if messages and messages[0]:
        print("\nSuccess! Received messages.")
        # Check for the subscription message
        sub_message = None
        for sender, message_list in messages[0].items():
            for msg in message_list:
                if msg['text'].strip().upper() == f"SUBSCRIBE {TEAM_NAME}":
                    sub_message = msg
                    break
            if sub_message:
                break

        if sub_message:
            print(f"\nFound the subscription message: {sub_message}")
            print(f"The user's number {TEST_USER_NUMBER} should now be registered with your team.")
        else:
            print(
                f"\nDidn't find the subscription message. Make sure the user sent 'SUBSCRIBE {TEAM_NAME}' to {HACKATHON_NUMBER}.")
    else:
        print("\nNo messages found. Make sure the user sent the subscription message to the hackathon number.")
else:
    print("Failed to send instructions to the user. Please check your team name and try again.")

print("\nTest complete. Please check the console output for results.")
