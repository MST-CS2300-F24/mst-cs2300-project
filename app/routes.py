from flask import Blueprint, request, redirect, url_for, render_template
import mysql.connector
from . import mysql

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

@app.route('/flights')
def flights():
    connection = mysql.connect()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM airports")
    airport_list = cursor.fetchall()
    cursor.execute("SELECT * FROM aircrafts")
    aircraft_list = cursor.fetchall()
    cursor.execute("SELECT * FROM flights")
    flight_list = cursor.fetchall()
    cursor.execute("SELECT * FROM maintenance_schedule")
    maintenance_schedule = cursor.fetchall()
    cursor.execute("SELECT * FROM maintenance_log")
    maintenance_log = cursor.fetchall()
    connection.close()
    return render_template('flights.html', airport_list=airport_list, aircraft_list=aircraft_list, flight_list=flight_list, maintenance_schedule=maintenance_schedule, maintenance_log=maintenance_log)

@app.route('/specific_airport')
def specific_airport():
    return render_template('specific_airport.html', icao_id=request.args.get('icao_id'))

@app.route('/specific_aircraft')
def specific_aircraft():
    return render_template('specific_aircraft.html', registration_code=request.args.get('registration_code'))

@app.route('/specific_flight')
def specific_flight():
    return render_template('specific_flight.html', id=request.args.get('id'))

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