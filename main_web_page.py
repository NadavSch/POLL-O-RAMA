# main_web_page.py

web_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Health Survey - {team_name}</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            line-height: 1.6;
            margin: 0;
            padding: 20px;
            background-color: #f4f4f4;
        }}
        .container {{
            max-width: 600px;
            margin: auto;
            background: white;
            padding: 20px;
            border-radius: 5px;
            box-shadow: 0 0 10px rgba(0,0,0,0.1);
        }}
        h1 {{
            color: #333;
            text-align: center;
        }}
        form {{
            margin-bottom: 20px;
        }}
        input[type="text"], input[type="tel"] {{
            width: 100%;
            padding: 8px;
            margin-bottom: 10px;
            border: 1px solid #ddd;
            border-radius: 4px;
        }}
        input[type="submit"], .button {{
            display: inline-block;
            background-color: #4CAF50;
            color: white;
            padding: 10px 20px;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            font-size: 16px;
            text-decoration: none;
        }}
        input[type="submit"]:hover, .button:hover {{
            background-color: #45a049;
        }}
        .button.admin {{
            background-color: #2196F3;
            display: block;
            width: 200px;
            margin: 20px auto;
            text-align: center;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>Health Survey - {team_name}</h1>
        <form action="/register" method="post">
            <input type="text" name="name" placeholder="Your Name" required>
            <input type="tel" name="phoneNumber" placeholder="Phone Number" required>
            <input type="submit" value="Register">
        </form>
        <form action="/unregister" method="post">
            <input type="tel" name="phoneNumber" placeholder="Phone Number" required>
            <input type="submit" value="Unregister">
        </form>
        <a href="/admin" class="button admin">Admin Panel</a>
    </div>
</body>
</html>
"""