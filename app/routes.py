from flask import Blueprint, request, redirect, url_for, render_template

app = Blueprint('app', __name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/airports')
def airports():
    return render_template('airports.html')

@app.route('/aircraft')
def aircraft():
    return render_template('aircraft.html')

@app.route('/manage')
def manage():
    return render_template('manage.html')

@app.route('/login')
def login():
    error = request.args.get('error')
    return render_template('login.html', error=error)

@app.route('/checklogin', methods=['POST'])
def checklogin():
    username = request.form['username']
    password = request.form['password']

    if username == 'admin' and password == 'CS2300':
        return redirect(url_for('app.home'))
    else:
        return redirect(url_for('app.login', error=True))