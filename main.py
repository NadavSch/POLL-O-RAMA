import error_html
import main_web_page
from flask import Flask, request
import requests

import success_html

app = Flask(__name__)

# The team name should be in uppercase and constant
TEAM_NAME = " TEAM NAME "

# Dictionary to store team data and phone numbers
team_data = {}


# Main route to display the form
@app.route('/')
def index():
    return main_web_page.web_HTML.format(team_name=TEAM_NAME)


# Route to handle the form and save data to the dictionary
@app.route('/register', methods=['POST'])
def register():
    phone_number = request.form['phoneNumber']

    # Save data to the dictionary
    team_data[TEAM_NAME] = phone_number

    # Send data to the specified URL
    response = requests.post(
        'http://hackathons.masterschool.com:3030/team/registerNumber',
        json={"teamName": TEAM_NAME, "phoneNumber": phone_number}
    )

    if response.status_code == 200:
        return success_html.success_result
    else:
        return error_html.error_result


if __name__ == '__main__':
    app.run(debug=True)
