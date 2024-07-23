from flask import Flask, request, send_file
from config import TEAM_NAME
import templates.error_html
import templates.main_web_page
import templates.success_html
import sms_api

app = Flask(__name__)


# Main route to display the form
@app.route('/')
def index():
  return templates.main_web_page.web_HTML.format(team_name=TEAM_NAME)


# Route to handle the form and save data to the dictionary
@app.route('/register', methods=['POST'])
def register():
  """
    Handle form submission to register a phone number and send an initial SMS.
    """
  phone_number = request.form['phoneNumber']
  response = sms_api.register_number(phone_number)
  if response:
    return templates.success_html.success_result
  else:
    return templates.error_html.error_result


@app.route('/results/<phone_number>')
def results(phone_number):
  """
        Display survey results for a specific phone number.
        """
  responses = sms_api.get_results(phone_number)
  if responses:
    return f"Your results: {responses}"
  return "No data."


@app.route('/chart')
def chart():
  """
        Generate and serve the pie chart image.
        """
  chart_path = sms_api.generate_pie_chart()
  return send_file(chart_path, mimetype='image/png')


if __name__ == '__main__':
  app.run(debug=True)
