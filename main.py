from flask import Flask, request, render_template_string, redirect, url_for, session, jsonify, send_file
import api
import error_html
import main_web_page
import success_html
import results_html
import admin_template
import logging
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)  # For session management

TEAM_NAME = "CTRL_ALT_DEFEAT"
ADMIN_PASSWORD = "hackathon2024"  # Simple password for the hackathon

logging.basicConfig(level=logging.INFO)


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
                        "message": "Failed to unregister phone number. It may not be registered or associated with "
                                   "this team."}), 400


@app.route('/results')
def results():
    overall_results = api.get_results()
    return render_template_string(results_html.results_template, results=overall_results)


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
        files = [f for f in os.listdir(directory) if f.startswith('survey_data_') and f.endswith('.json')]
        if not files:
            return "No data files available", 404
        latest_file = max(files)
        return send_file(os.path.join(directory, latest_file), as_attachment=True)
    else:
        return redirect(url_for('admin_panel', error="Authentication required"))


@app.route('/logout')
def logout():
    session.pop('authenticated', None)
    return redirect(url_for('admin_panel'))


if __name__ == '__main__':
    app.run(debug=True)