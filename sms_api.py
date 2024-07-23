import requests
import matplotlib.pyplot as plt
from config import API_BASE_URL, TEAM_NAME


# Dictionary of surveys with one question each
SURVEYS = {
    "1": "How old are you? Reply with a number:\n1. 0-12\n2. 13-25\n3. 26-60\n4. 61+",
    "2": "How often do you exercise? Reply with a number:\n1. Daily\n2. 2-3 times a week\n3. Once a week\n4. Rarely",
    "3": "How would you rate your overall health? Reply with a number:\n1. Excellent\n2. Good\n3. Fair\n4. Poor"
}

# Dictionary to store user data and survey responses
user_data = {}


def register_number(phone_number):
    """
    Register a phone number with the API and send an initial SMS.

    Args:
    phone_number (str): The phone number to register.

    Returns:
    bool: True if registration was successful, False otherwise.
    """
    endpoint = f"{API_BASE_URL}/team/registerNumber"
    data = {"phoneNumber": phone_number, "teamName": TEAM_NAME}
    response = requests.post(endpoint, json=data)
    if response.status_code == 200:
        welcome_msg = ("Welcome to our health survey! To start, reply with:\n'1' for Age survey\n'2' for Exercise "
                       "survey\n'3' for Overall Health survey")
        send_sms(phone_number, welcome_msg)
        user_data[phone_number] = {"responses": {}}
        return True
    return False


def send_sms(phone_number, message):
    """
    Send an SMS message to a phone number.

    Args:
    phone_number (str): The recipient's phone number.
    message (str): The message to send.

    Returns:
    bool: True if the message was sent successfully, False otherwise.
    """
    endpoint = f"{API_BASE_URL}/sms/send"
    data = {"phoneNumber": phone_number, "message": message, "sender": "Pollorama"}
    response = requests.post(endpoint, json=data)
    return response.status_code == 200


def get_messages():
    """
    Retrieve all messages for the team from the API.

    Returns:
    list: A list of message dictionaries if successful, an empty list otherwise.
    """
    endpoint = f"{API_BASE_URL}/team/getMessages/{TEAM_NAME}"
    response = requests.get(endpoint)
    if response.status_code == 200:
        return response.json()
    return []


def process_message(phone_number, message):
    """
    Process an incoming message, either starting a survey or recording a response.

    Args:
    phone_number (str): The sender's phone number.
    message (str): The received message.

    Returns:
    str: The next question, a completion message, or an error message.
    """
    if phone_number not in user_data:
        return "Please register first by visiting our website."

    message = message.strip()

    if message in SURVEYS:
        # User is starting a new survey
        return SURVEYS[message]
    elif message.upper() in ['A', 'B', 'C', 'D']:
        # User is answering a survey question
        for survey_num, question in SURVEYS.items():
            if question not in user_data[phone_number]["responses"]:
                user_data[phone_number]["responses"][question] = message.upper()
                return (f"Thank you for your response. To take another survey, reply with '1', '2', or '3'.\nOr view "
                        f"your results at: http://yourwebsite.com/results/{phone_number}")
        return "You've completed all surveys. To retake a survey, reply with '1', '2', or '3'."
    else:
        return ("Invalid response. Please reply with '1', '2', or '3' to start a survey, or A, B, C, or D to answer a "
                "question.")


def get_results(phone_number):
    """
    Get the results of all surveys taken by a user.

    Args:
    phone_number (str): The phone number of the respondent.

    Returns:
    dict: A dictionary containing the questions and responses for all surveys taken.
    """
    if phone_number in user_data:
        return user_data[phone_number]["responses"]
    return None


def generate_pie_chart():
    """
    Generate a pie chart based on user responses.

    Returns:
    str: Path to the saved pie chart image.
    """
    age_responses = [user_data[user]["responses"].get(SURVEYS["1"], None) for user in user_data]
    age_responses = [resp for resp in age_responses if resp]

    labels = ['0-12', '13-25', '26-60', '61+']
    sizes = [age_responses.count(str(i)) for i in range(1, 5)]

    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
    ax1.axis('equal')

    plt.savefig('static/images/pie_chart.png')
    return 'static/images/pie_chart.png'