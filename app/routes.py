from flask import Blueprint, request, redirect, url_for, render_template

app = Blueprint('app', __name__)

@app.route('/')
def home():
    error = request.args.get('error')
    return render_template('home.html', error=error)

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    if username == 'admin' and password == 'CS2300':
        return redirect(url_for('app.site'))
    else:
        return redirect(url_for('app.home', error=True))

@app.route('/site')
def site():
    return render_template('site.html')

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