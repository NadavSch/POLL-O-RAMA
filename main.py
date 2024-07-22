from flask import Flask, request
import requests

app = Flask(__name__)

# The team name should be in uppercase and constant
TEAM_NAME = " TEAM NAME "

# Dictionary to store team data and phone numbers
team_data = {}


# Main route to display the form
@app.route('/')
def index():
  return '''
        <h1>Register Team Number</h1>
        <form method="POST" action="/register">
            Enter Name: <input type="text" name="teamName" value="{team_name}" readonly><br>
            Enter Phone Number: <input type="text" name="phoneNumber"><br>
            <input type="submit" value="Register">
        </form>
    '''.format(team_name=TEAM_NAME)


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
    return "Team registered successfully"
  else:
    return "Failed to register team"


if __name__ == '__main__':
  app.run(debug=True)
