from flask import Flask, render_template_string
import json
from results_html import results_html

app = Flask(__name__)

# Sample survey data
user_data = {
    "1234567890": {
        "name": "John Doe",
        "responses": ["A", "B", "C"],
        "survey_started": True,
        "registration_time": "2023-07-24T10:30:00Z",
        "last_processed_time": "2023-07-24T11:00:00Z"
    },
    "0987654321": {
        "name": "Jane Smith",
        "responses": ["B", "C", "D"],
        "survey_started": True,
        "registration_time": "2023-07-24T11:30:00Z",
        "last_processed_time": "2023-07-24T12:00:00Z"
    },
    "1111111111": {
        "name": "Alice Johnson",
        "responses": ["C", "A", "B"],
        "survey_started": True,
        "registration_time": "2023-07-24T13:30:00Z",
        "last_processed_time": "2023-07-24T14:00:00Z"
    },
    "2222222222": {
        "name": "Bob Williams",
        "responses": ["D", "D", "A"],
        "survey_started": True,
        "registration_time": "2023-07-24T15:30:00Z",
        "last_processed_time": "2023-07-24T16:00:00Z"
    },
    "3333333333": {
        "name": "Charlie Brown",
        "responses": ["A", "C", "D"],
        "survey_started": True,
        "registration_time": "2023-07-24T17:30:00Z",
        "last_processed_time": "2023-07-24T18:00:00Z"
    }
}


def aggregate_survey_data():
    age_groups = {"A": "18-25", "B": "26-35", "C": "36-45", "D": "46+"}
    exercise_freq = {"A": "Daily", "B": "2-3 times a week", "C": "Once a week", "D": "Rarely"}
    health_rating = {"A": "Excellent", "B": "Good", "C": "Fair", "D": "Poor"}

    data_by_age = {
        "18-25": {"exercise": {v: 0 for v in exercise_freq.values()}, "health": {v: 0 for v in health_rating.values()}},
        "26-35": {"exercise": {v: 0 for v in exercise_freq.values()}, "health": {v: 0 for v in health_rating.values()}},
        "36-45": {"exercise": {v: 0 for v in exercise_freq.values()}, "health": {v: 0 for v in health_rating.values()}},
        "46+": {"exercise": {v: 0 for v in exercise_freq.values()}, "health": {v: 0 for v in health_rating.values()}},
    }

    for data in user_data.values():
        responses = data["responses"]
        age_group = age_groups.get(responses[0], "Unknown")
        exercise = exercise_freq.get(responses[1], "Unknown")
        health = health_rating.get(responses[2], "Unknown")

        if age_group in data_by_age:
            data_by_age[age_group]["exercise"][exercise] += 1
            data_by_age[age_group]["health"][health] += 1

    return data_by_age


@app.route('/')
@app.route('/results')
def results():
    aggregated_data = aggregate_survey_data()
    return render_template_string(results_html, aggregated_data=json.dumps(aggregated_data))


if __name__ == '__main__':
    app.run(debug=True, port=5000)
