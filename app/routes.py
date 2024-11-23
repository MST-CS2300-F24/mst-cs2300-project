from flask import Blueprint, request, redirect, url_for, render_template, flash
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
    connection = mysql.connect()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM airports")
    airport_list = cursor.fetchall()
    connection.close()
    return render_template('airports.html', airport_list=airport_list)

@app.route('/aircraft')
def aircraft():
    connection = mysql.connect()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM aircrafts")
    aircraft_list = cursor.fetchall()
    connection.close()
    return render_template('aircraft.html', aircraft_list=aircraft_list)

@app.route('/flights')
def flights():
    connection = mysql.connect()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM flights")
    flight_list = cursor.fetchall()
    connection.close()
    return render_template('flights.html', flight_list=flight_list)

@app.route('/specific_airport')
def specific_airport():
    return render_template('specific_airport.html', icao_id=request.args.get('icao_id'))

@app.route('/specific_aircraft')
def specific_aircraft():
    return render_template('specific_aircraft.html', registration_code=request.args.get('registration_code'))

@app.route('/specific_flight')
def specific_flight():
    return render_template('specific_flight.html', id=request.args.get('id'))

@app.route('/add')
def add():
    return render_template('add.html')

@app.route('/add_aircraft', methods=['GET', 'POST'])
def add_aircraft():
    if request.method == 'POST':
        # Process form data
        registration_code = request.form['registration_code']
        flight_range = request.form['flight_range']
        model = request.form['model']
        weight_capacity = request.form['weight_capacity']
        fuel_capacity = request.form['fuel_capacity']
        passenger_capacity = request.form['passenger_capacity']
        fuel_efficiency = request.form['fuel_efficiency']
        status = request.form['status']
        manufacturer = request.form['manufacturer']
        manufacture_date = request.form['manufacture_date']
        home_airport_id = request.form['home_airport_id']
        latest_arrival_airport_id = request.form['latest_arrival_airport_id']

        #fix nulls
        if registration_code == '':
            registration_code = None
        if flight_range == '':
            flight_range = None
        if model == '':
            model = None
        if weight_capacity == '':
            weight_capacity = None
        if fuel_capacity == '':
            fuel_capacity = None
        if passenger_capacity == '':
            passenger_capacity = None
        if fuel_efficiency == '':
            fuel_efficiency = None
        if status == '':
            status = None
        if manufacturer == '':
            manufacturer = None
        if manufacture_date == '':
            manufacture_date = None
        if home_airport_id == '':
            home_airport_id = None
        if latest_arrival_airport_id == '':
            latest_arrival_airport_id = None

        connection = mysql.connect()
        cursor = connection.cursor()
        cursor.execute("INSERT INTO aircrafts (registration_code, flight_range, model, weight_capacity, fuel_capacity, passenger_capacity, fuel_efficiency, status, manufacturer, manufacture_date, home_airport_id, latest_arrival_airport_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (registration_code, flight_range, model, weight_capacity, fuel_capacity, passenger_capacity, fuel_efficiency, status, manufacturer, manufacture_date, home_airport_id, latest_arrival_airport_id))
        connection.commit()
        connection.close()

        return redirect(url_for('app.add_aircraft'))
    return render_template('add_aircraft.html')

@app.route('/add_airport', methods=['GET', 'POST'])
def add_airport():
    if request.method == 'POST':
        # Process form data
        icao_id = request.form['icao_code']
        civilian_name = request.form['civilian_name']
        latitude = request.form['latitude']
        longitude = request.form['longitude']

        #fix nulls
        if icao_id == '':
            icao_id = None
        if civilian_name == '':
            civilian_name = None
        if latitude == '':
            latitude = None
        if longitude == '':
            longitude = None
        
        
        connection = mysql.connect()
        cursor = connection.cursor()
        cursor.execute("INSERT INTO airports (icao_id, civilian_name, latitude, longitude) VALUES (%s, %s, %s, %s)", (icao_id, civilian_name, latitude, longitude))
        connection.commit()
        connection.close()

        return redirect(url_for('app.add_airport'))
    return render_template('add_airport.html')

@app.route('/add_flight', methods=['GET', 'POST'])
def add_flight():
    if request.method == 'POST':
        # Process form data
        scheduled_departure = request.form['scheduled_departure']
        scheduled_arrival = request.form['scheduled_arrival']
        actual_departure = request.form['actual_departure']
        actual_arrival = request.form['actual_arrival']
        passenger_count = request.form['passenger_count']
        projected_fuel_consumption = request.form['projected_fuel_consumption']
        actual_fuel_consumption = request.form['actual_fuel_consumption']
        distance = request.form['distance']
        aircraft_id = request.form['aircraft_id']
        destination_airport_id = request.form['destination_airport_id']
        origin_airport_id = request.form['origin_airport_id']

        #reformat datetimes as YYYY-MM-DD hh:mm:ss
        if scheduled_departure == '':
            scheduled_departure = None
        else:
            scheduled_departure = scheduled_departure.replace('T', ' ')
            scheduled_departure = scheduled_departure + ':00'
        if scheduled_arrival == '':
            scheduled_arrival = None
        else:
            scheduled_arrival = scheduled_arrival.replace('T', ' ')
            scheduled_arrival = scheduled_arrival + ':00'
        if actual_departure == '':
            actual_departure = None
        else:
            actual_departure = actual_departure.replace('T', ' ')
            actual_departure = actual_departure + ':00'
        if actual_arrival == '':
            actual_arrival = None
        else:
            actual_arrival = actual_arrival.replace('T', ' ')
            actual_arrival = actual_arrival + ':00'
        
        #fix nulls
        if passenger_count == '':
            passenger_count = None
        if projected_fuel_consumption == '':
            projected_fuel_consumption = None
        if actual_fuel_consumption == '':
            actual_fuel_consumption = None
        if distance == '':
            distance = None
        if aircraft_id == '':
            aircraft_id = None
        if destination_airport_id == '':
            destination_airport_id = None
        
        print(scheduled_departure, scheduled_arrival, actual_departure, actual_arrival, passenger_count, projected_fuel_consumption, actual_fuel_consumption, distance, aircraft_id, destination_airport_id, origin_airport_id)


        connection = mysql.connect()
        cursor = connection.cursor()
        cursor.execute("INSERT INTO flights (scheduled_departure, scheduled_arrival, actual_departure, actual_arrival, passenger_count, projected_fuel_consumption, actual_fuel_consumption, distance, aircraft_id, destination_airport_id, origin_airport_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (scheduled_departure, scheduled_arrival, actual_departure, actual_arrival, passenger_count, projected_fuel_consumption, actual_fuel_consumption, distance, aircraft_id, destination_airport_id, origin_airport_id))
        connection.commit()
        connection.close()

        return redirect(url_for('app.add_flight'))
    return render_template('add_flight.html')

@app.route('/add_maintenance_log', methods=['GET', 'POST'])
def add_maintenance_log():
    if request.method == 'POST':
        # Process form data
        service_start = request.form['service_start']
        service_finish = request.form['service_finish']
        description = request.form['description']
        aircraft_id = request.form['aircraft_id']
        maintenance_location = request.form['maintenance_location']

        #fix nulls
        if service_start == '':
            service_start = None
        if service_finish == '':
            service_finish = None
        if description == '':
            description = None
        if aircraft_id == '':
            aircraft_id = None
        if maintenance_location == '':
            maintenance_location = None

        connection = mysql.connect()
        cursor = connection.cursor()
        cursor.execute("INSERT INTO maintenance_log (service_start, service_finish, description, aircraft_id, maintenance_location) VALUES (%s, %s, %s, %s, %s)", (service_start, service_finish, description, aircraft_id, maintenance_location))
        connection.commit()
        connection.close()
        
        return redirect(url_for('app.add_maintenance_log'))
    return render_template('add_maintenance_log.html')

@app.route('/add_schedule_maintenance', methods=['GET', 'POST'])
def add_schedule_maintenance():
    if request.method == 'POST':
        # Process form data
        suggested_date = request.form['suggested_date']
        description = request.form['description']
        aircraft_id = request.form['aircraft_id']
        maintenance_location = request.form['maintenance_location']

        #fix nulls
        if suggested_date == '':
            suggested_date = None
        if description == '':
            description = None
        if aircraft_id == '':
            aircraft_id = None
        if maintenance_location == '':
            maintenance_location = None

        connection = mysql.connect()
        cursor = connection.cursor()
        cursor.execute("INSERT INTO maintenance_schedule (suggested_date, description, aircraft_id, maintenance_location) VALUES (%s, %s, %s, %s)", (suggested_date, description, aircraft_id, maintenance_location))
        connection.commit()
        connection.close()

        return redirect(url_for('app.add_schedule_maintenance'))
    return render_template('add_schedule_maintenance.html')

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