from flask import Flask, request, redirect, url_for, render_template_string

app = Flask(__name__)

@app.route('/')
def home():
    error = request.args.get('error')
    return render_template_string('''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Login</title>
        <style>
            body {
                background-image: url('/static/media/images/homepage.webp');
                background-size: cover;
                background-repeat: no-repeat;
                background-position: center;
                margin: 0;
                font-family: Arial, sans-serif;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                color: #333;
            }

            .login-container {
                background-color: rgba(255, 255, 255, 0.8);
                padding: 20px;
                border-radius: 10px;
                box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
                text-align: center;
                width: 400px;
            }

            .login-container input[type="text"],
            .login-container input[type="password"] {
                width: 100%;
                padding: 10px;
                margin: 10px 0;
                border: 1px solid #ccc;
                border-radius: 5px;
                box-sizing: border-box;
            }

            .login-container input[type="submit"] {
                background-color: #333;
                color: white;
                padding: 10px 20px;
                border: none;
                border-radius: 5px;
                cursor: pointer;
            }

            .login-container input[type="submit"]:hover {
                background-color: #555;
            }
        </style>
    </head>
    <body>
        <div class="login-container">
            <h2>Login</h2>
            <form action="/login" method="post">
                <label for="username">Username:</label><br>
                <input type="text" id="username" name="username"><br>
                <label for="password">Password:</label><br>
                <input type="password" id="password" name="password"><br><br>
                <input type="submit" value="Login">
            </form>
        </div>
        {% if error %}
        <script>
            alert("Invalid credentials, please try again.");
        </script>
        {% endif %}
    </body>
    </html>
    ''', error=error)

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    if username == 'admin' and password == 'CS2300':
        return redirect(url_for('site'))
    else:
        return redirect(url_for('home', error=True))

@app.route('/site')
def site():
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Site</title>
        <style>
            body {
                background-image: url('/static/media/images/homepage.webp');
                background-size: cover;
                background-repeat: no-repeat;
                background-position: center;
                margin: 0;
                font-family: Arial, sans-serif;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                color: #333;
            }

            .navbar {
                overflow: hidden;
                background-color: #333;
                position: absolute;
                top: 0;
                width: 100%;
            }

            .navbar a {
                float: left;
                display: block;
                color: #f2f2f2;
                text-align: center;
                padding: 14px 16px;
                text-decoration: none;
            }

            .navbar a:hover {
                background-color: #ddd;
                color: black;
            }

            .content {
                text-align: center;
            }

            .masthead {
                position: absolute;
                bottom: 0;
                width: 100%;
                background-color: rgba(0, 0, 0, 0.5);
                color: white;
                text-align: center;
                padding: 10px 0;
            }
        </style>
    </head>
    <body>
        <div class="navbar">
            <a href="#home">Home</a>
            <a href="#dashboard">Dashboard</a>
            <a href="#aircraft">Aircraft</a>
            <a href="#airports">Airports</a>
            <a href="#manage">Manage</a>
        </div>
        <div class="content">
            <h1>CS2300 Final Project</h1>
            <p>We hope you enjoy!.</p>
        </div>
        <div class="masthead">
            <p>Luke Roth and Rohith Velmurugan 2024</p>
        </div>
    </body>
    </html>
    '''

if __name__ == '__main__':
    app.run(debug=True)