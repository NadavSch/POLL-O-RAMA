from flask import Flask, request, render_template_string, redirect, url_for, session, jsonify, send_file
import api
import error_html
import main_web_page
import success_html
import results_html
import admin_template
import logging
import os
import json

app = Flask(__name__)
app.secret_key = os.urandom(24)  # For session management

TEAM_NAME = "CTRL_ALT_DEFEAT"
ADMIN_PASSWORD = "hackathon2024"  # Simple password for the hackathon

logging.basicConfig(level=logging.INFO)


def aggregate_survey_data(user_data):
    logging.info("Starting data aggregation")
    logging.info("Number of users in data: %d", len(user_data))

    age_groups = {"A": "18-25", "B": "26-35", "C": "36-45", "D": "46+"}
    exercise_freq = {"A": "Daily", "B": "2-3 times a week", "C": "Once a week", "D": "Rarely"}
    health_rating = {"A": "Excellent", "B": "Good", "C": "Fair", "D": "Poor"}

    data_by_age = {
        "18-25": {"exercise": {v: 0 for v in exercise_freq.values()}, "health": {v: 0 for v in health_rating.values()}},
        "26-35": {"exercise": {v: 0 for v in exercise_freq.values()}, "health": {v: 0 for v in health_rating.values()}},
        "36-45": {"exercise": {v: 0 for v in exercise_freq.values()}, "health": {v: 0 for v in health_rating.values()}},
        "46+": {"exercise": {v: 0 for v in exercise_freq.values()}, "health": {v: 0 for v in health_rating.values()}},
    }

    for phone, data in user_data.items():
        responses = data.get("responses", [])
        logging.info("Processing responses for user %s: %s", phone, responses)

        if len(responses) == 3:  # Ensure we have all 3 responses
            age_group = age_groups.get(responses[0], "Unknown")
            exercise = exercise_freq.get(responses[1], "Unknown")
            health = health_rating.get(responses[2], "Unknown")

            if age_group in data_by_age:
                data_by_age[age_group]["exercise"][exercise] += 1
                data_by_age[age_group]["health"][health] += 1
        else:
            logging.warning("Incomplete responses for user %s: %s", phone, responses)

    logging.info("Aggregated data: %s", data_by_age)
    return data_by_age


@app.route('/')
def index():
    return main_web_page.web_HTML.format(team_name=TEAM_NAME)


@app.route('/register', methods=['POST'])
def register():
    name = request.form['name']
    phone_number = request.form['phoneNumber']
    if api.register_number(name, phone_number):
        return render_template_string(success_html.success_result)
    else:
        error_message = "Failed to register. Please check your phone number and try again."
        return render_template_string(error_html.error_result, error_message=error_message)


@app.route('/unregister', methods=['POST'])
def unregister():
    phone_number = request.form['phoneNumber']
    if api.unregister_number(phone_number):
        return jsonify({"status": "success", "message": "Phone number unregistered successfully"}), 200
    else:
        return jsonify({"status": "error",
                        "message": "Failed to unregister phone number. It may not be registered or associated with this team."}), 400


@app.route('/admin', methods=['GET', 'POST'])
def admin_panel():
    if request.method == 'POST':
        password = request.form['password']
        if password == ADMIN_PASSWORD:
            session['authenticated'] = True
            registered_users = len(api.get_user_data())
            return render_template_string(admin_template.admin_template, authenticated=True,
                                          registered_users=registered_users)
        else:
            return render_template_string(admin_template.admin_template, error="Incorrect password",
                                          authenticated=False)

    authenticated = session.get('authenticated', False)
    registered_users = len(api.get_user_data()) if authenticated else 0
    message = request.args.get('message')
    error = request.args.get('error')

    return render_template_string(admin_template.admin_template,
                                  authenticated=authenticated,
                                  registered_users=registered_users,
                                  message=message,
                                  error=error)


@app.route('/start_survey', methods=['POST'])
def start_survey():
    if 'authenticated' in session and session['authenticated']:
        api.start_survey()
        return redirect(url_for('admin_panel', message="Survey started for all registered users"))
    else:
        return redirect(url_for('admin_panel', error="Authentication required"))


@app.route('/process_messages', methods=['POST'])
def process_messages():
    if 'authenticated' in session and session['authenticated']:
        result = api.trigger_process_messages()
        return redirect(url_for('admin_panel', message=result))
    else:
        return redirect(url_for('admin_panel', error="Authentication required"))


@app.route('/download_data')
def download_data():
    if 'authenticated' in session and session['authenticated']:
        directory = os.path.dirname(os.path.abspath(__file__))
        json_file = os.path.join(directory, 'survey_data.json')
        if not os.path.exists(json_file):
            return "No data file available", 404
        return send_file(json_file, as_attachment=True)
    else:
        return redirect(url_for('admin_panel', error="Authentication required"))


@app.route('/view_results')
def view_results():
    if 'authenticated' in session and session['authenticated']:
        directory = os.path.dirname(os.path.abspath(__file__))
        json_file = os.path.join(directory, 'survey_data.json')

        logging.info(f"Looking for JSON file at: {json_file}")

        if not os.path.exists(json_file):
            logging.error(f"JSON file not found at: {json_file}")
            return "No data file available", 404

        try:
            with open(json_file, 'r') as f:
                user_data = json.load(f)

            if not user_data:
                logging.error("Loaded JSON file is empty")
                return "No survey data available", 404

            logging.info(f"Successfully loaded data from JSON file. Data: {user_data}")
            aggregated_data = aggregate_survey_data(user_data)

            if not any(aggregated_data.values()):
                logging.error("Aggregated data is empty")
                return "No valid survey responses found", 404

            return render_template_string(results_html.results_html, aggregated_data=json.dumps(aggregated_data))

        except json.JSONDecodeError as e:
            logging.error(f"Failed to parse JSON from file: {json_file}. Error: {str(e)}")
            return "Error reading survey data", 500
        except Exception as e:
            logging.error(f"Unexpected error when processing survey data: {str(e)}")
            return "Unexpected error occurred", 500
    else:
        return redirect(url_for('admin_panel', error="Authentication required"))


@app.route('/logout')
def logout():
    session.pop('authenticated', None)
    return redirect(url_for('admin_panel'))


if __name__ == '__main__':
    app.run(debug=True)