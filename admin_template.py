admin_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Admin Panel - Health Survey</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            line-height: 1.6;
            margin: 0;
            padding: 20px;
            background-color: #f4f4f4;
        }
        .container {
            max-width: 600px;
            margin: auto;
            background: white;
            padding: 20px;
            border-radius: 5px;
            box-shadow: 0 0 10px rgba(0,0,0,0.1);
        }
        h1 {
            color: #333;
            text-align: center;
            margin-top: 0;
        }
        .info {
            background-color: #e7f3fe;
            border-left: 6px solid #2196F3;
            margin-bottom: 15px;
            padding: 4px 12px;
        }
        .button {
            background-color: #4CAF50;
            border: none;
            color: white;
            padding: 15px 32px;
            text-align: center;
            text-decoration: none;
            display: block;
            font-size: 16px;
            margin: 10px 0;
            cursor: pointer;
            border-radius: 5px;
            width: 100%;
            box-sizing: border-box;
        }
        .button.process {
            background-color: #2196F3;
        }
        .button.download {
            background-color: #FF9800;
        }
        .button.logout {
            background-color: #f44336;
        }
        .button.view-results {
            background-color: #9C27B0;
        }
        .error {
            color: red;
            text-align: center;
        }
        .message {
            color: green;
            text-align: center;
        }
        input[type="password"] {
            width: 100%;
            padding: 12px 20px;
            margin: 8px 0;
            display: inline-block;
            border: 1px solid #ccc;
            border-radius: 4px;
            box-sizing: border-box;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Admin Panel - Health Survey</h1>
        {% if error %}
            <p class="error">{{ error }}</p>
        {% endif %}
        {% if message %}
            <p class="message">{{ message }}</p>
        {% endif %}
        {% if not authenticated %}
            <form method="post">
                <label for="password">Admin Password:</label>
                <input type="password" id="password" name="password" required>
                <input type="submit" value="Login" class="button">
            </form>
        {% else %}
            <div class="info">
                <p>Registered Users: {{ registered_users }}</p>
            </div>
            <form action="{{ url_for('start_survey') }}" method="post">
                <input type="submit" value="Start Survey" class="button">
            </form>
            <form action="{{ url_for('process_messages') }}" method="post">
                <input type="submit" value="Process Messages" class="button process">
            </form>
            <a href="{{ url_for('download_data') }}" class="button download">Download Latest Data</a>
            <a href="{{ url_for('view_results') }}" class="button view-results">View Results</a>
            <a href="{{ url_for('logout') }}" class="button logout">Logout</a>
        {% endif %}
    </div>
</body>
</html>
"""