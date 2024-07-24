# api.py

import requests
import logging
from datetime import datetime, timezone

logging.basicConfig(level=logging.INFO)

API_BASE_URL = "http://hackathons.masterschool.com:3030"
TEAM_NAME = "CTRL_ALT_DEFEAT"
HACKATHON_NUMBER = "491771786208"  # The hackathon's number without the '+' sign

SURVEY = [
    "1. What is your age group? Reply with A (18-25), B (26-35), C (36-45), D (46+)",
    "2. How often do you exercise? A (Daily), B (2-3 times a week), C (Once a week), D (Rarely)",
    "3. How would you rate your overall health? A (Excellent), B (Good), C (Fair), D (Poor)"
]

# In-memory storage for user data and overall results
user_data = {}


def get_user_data():
    return user_data


def register_number(name, phone_number):
    logging.info(f"Preparing registration for: {phone_number} for {name}")

    if phone_number in user_data:
        logging.info(f"Clearing existing data for {phone_number}")
        del user_data[phone_number]

    endpoint = f"{API_BASE_URL}/team/registerNumber"
    data = {"phoneNumber": phone_number, "teamName": TEAM_NAME}
    try:
        response = requests.post(endpoint, json=data)
        logging.info(f"Register API response status: {response.status_code}")
        logging.info(f"Register API response content: {response.text}")

        if response.status_code != 200 and "already exists" not in response.text:
            logging.error(f"Failed to register number with API. Status code: {response.status_code}")
            return False
    except Exception as e:
        logging.error(f"An error occurred during API registration: {str(e)}")
        return False

    welcome_msg = (
        f"Welcome {name} to our health survey! You have been registered. "
        f"Please wait for the survey to start. You will receive all questions at once when it begins."
    )

    if send_sms(phone_number, welcome_msg):
        registration_time = datetime.now(timezone.utc).isoformat()
        user_data[phone_number] = {
            "name": name,
            "responses": [],
            "survey_started": False,
            "registration_time": registration_time,
            "last_processed_time": registration_time
        }
        logging.info(f"User data created for {phone_number} with registration time set to {registration_time}")
        logging.info(f"Current user_data: {user_data}")
        return True
    else:
        logging.error(f"Failed to send SMS to {phone_number}")
        return False


def unregister_number(phone_number):
    logging.info(f"Attempting to unregister number: {phone_number}")
    endpoint = f"{API_BASE_URL}/team/unregisterNumber"
    data = {"phoneNumber": phone_number, "teamName": TEAM_NAME}
    try:
        response = requests.post(endpoint, json=data)
        logging.info(f"Unregister API response status: {response.status_code}")
        logging.info(f"Unregister API response content: {response.text}")
        if response.status_code == 200:
            if phone_number in user_data:
                del user_data[phone_number]
            logging.info(f"User data cleared for {phone_number}")
            return True
        else:
            logging.error(f"Unregistration failed with status code: {response.status_code}")
            return False
    except Exception as e:
        logging.error(f"An error occurred during unregistration: {str(e)}")
        return False


def send_sms(phone_number, message):
    logging.info(f"Attempting to send SMS to: {phone_number}")
    logging.info(f"Message content: {message}")
    endpoint = f"{API_BASE_URL}/sms/send"
    data = {
        "phoneNumber": phone_number,
        "message": message,
        "sender": HACKATHON_NUMBER
    }
    try:
        logging.info(f"Sending request to {endpoint} with data: {data}")
        response = requests.post(endpoint, json=data)
        logging.info(f"SMS API response status: {response.status_code}")
        logging.info(f"SMS API response content: {response.text}")

        if response.status_code == 200:
            response_json = response.json()
            logging.info(f"Full API response: {response_json}")
            if 'messages' in response_json and len(response_json['messages']) > 0:
                message_status = response_json['messages'][0]['status']['name']
                message_description = response_json['messages'][0]['status']['description']
                logging.info(f"Message status: {message_status}")
                logging.info(f"Message description: {message_description}")
                if message_status == "PENDING_ACCEPTED":
                    logging.info(f"SMS to {phone_number} accepted for delivery")
                    return True
                else:
                    logging.error(
                        f"SMS to {phone_number} not accepted. Status: {message_status}, Description: {message_description}")
                    return False
            else:
                logging.error(f"Unexpected response format from SMS API: {response.text}")
                return False
        else:
            logging.error(f"SMS API returned non-200 status code: {response.status_code}")
            return False
    except Exception as e:
        logging.error(f"An error occurred while sending SMS: {str(e)}")
        return False


def process_message(phone_number, message):
    logging.info(f"Processing message from {phone_number}: {message}")
    if phone_number not in user_data:
        logging.warning(f"Unregistered number {phone_number} attempting to use the service")
        return None

    user = user_data[phone_number]
    message = message.strip().upper()
    logging.info(f"Processed message: {message}")

    if not user["survey_started"]:
        return "The survey has not started yet. Please wait for all questions to be sent to you."

    # Process all answers at once
    answers = message.split(',')
    if len(answers) != len(SURVEY):
        return f"Please provide {len(SURVEY)} answers separated by commas."

    user["responses"] = answers
    logging.info(f"Answers recorded for user {phone_number}: {answers}")
    return "Thank you for completing the survey!"


def get_results():
    return user_data


def start_survey():
    all_questions = "\n".join(SURVEY)
    survey_message = (f"The health survey is starting now. Please answer all questions in one message, separating your "
                      f"answers with commas. For example: A,B,C\n\n{all_questions}")

    for phone_number, user in user_data.items():
        user['survey_started'] = True
        send_sms(phone_number, survey_message)


def trigger_process_messages():
    logging.info(f"Current user_data at start of trigger_process_messages: {user_data}")
    endpoint = f"{API_BASE_URL}/team/getMessages/{TEAM_NAME}"
    try:
        response = requests.get(endpoint)
        if response.status_code == 200:
            messages = response.json()
            logging.info(f"Fetched messages: {messages}")

            if isinstance(messages, list):
                logging.info(f"Fetched {len(messages)} message groups")
                for message_group in messages:
                    for phone_number, message_list in message_group.items():
                        if phone_number in user_data:
                            logging.info(f"Processing messages for registered user {phone_number}")
                            last_processed_time = datetime.fromisoformat(
                                user_data[phone_number].get('last_processed_time',
                                                            user_data[phone_number]['registration_time']))

                            # Filter messages received after last processed time
                            new_messages = [
                                msg for msg in message_list
                                if datetime.fromisoformat(msg['receivedAt']) > last_processed_time
                            ]

                            if new_messages:
                                logging.info(f"Found {len(new_messages)} new messages for {phone_number}")
                                # Process only the most recent message
                                latest_message = max(new_messages, key=lambda x: x['receivedAt'])
                                logging.info(
                                    f"Processing latest message: {latest_message['text']} (received at {latest_message['receivedAt']})")
                                response = process_message(phone_number, latest_message['text'])
                                if response:
                                    send_sms(phone_number, response)
                                user_data[phone_number]['last_processed_time'] = latest_message['receivedAt']
                            else:
                                logging.info(f"No new messages to process for {phone_number}")
                        else:
                            logging.info(f"Skipping messages for unregistered number {phone_number}")
            else:
                logging.error(f"Unexpected message format: {type(messages)}")
        else:
            logging.error(f"Failed to fetch messages. Status code: {response.status_code}")
    except Exception as e:
        logging.error(f"An error occurred while fetching messages: {str(e)}")
        logging.exception("Exception details:")

    return "Messages processed"
