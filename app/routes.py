from flask import Blueprint, request, redirect, url_for, render_template, flash
import mysql.connector
from . import mysql

app = Blueprint('app', __name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/dashboard')
def dashboard():
    connection = mysql.connect()
    cursor = connection.cursor()

    # Overall average flights per plane
    cursor.execute("""
        SELECT AVG(flight_count) AS overall_avg_flights
        FROM (
            SELECT COUNT(*) AS flight_count
            FROM flights
            GROUP BY aircraft_id
        ) AS subquery
    """)
    overall_avg_flights = "{:.2f}".format(cursor.fetchone()[0])

    # Most flown aircraft
    cursor.execute("""
        SELECT aircraft_id, COUNT(*) AS flight_count
        FROM flights
        GROUP BY aircraft_id
        ORDER BY flight_count DESC
        LIMIT 3
    """)
    most_flown_aircraft = cursor.fetchall()

    # Most visited airports
    cursor.execute("""
        SELECT origin_airport_id, COUNT(*) AS visit_count
        FROM flights
        GROUP BY origin_airport_id
        ORDER BY visit_count DESC
        LIMIT 3
    """)
    most_visited_airports = cursor.fetchall()

    # Least visited airports
    cursor.execute("""
        SELECT origin_airport_id, COUNT(*) AS visit_count
        FROM flights
        GROUP BY origin_airport_id
        ORDER BY visit_count ASC
        LIMIT 3
    """)
    least_visited_airports = cursor.fetchall()

    # Number of scheduled maintenances in the coming week
    cursor.execute("""
        SELECT COUNT(*) AS maintenance_count
        FROM maintenance_schedule
        WHERE suggested_date >= CURDATE() AND suggested_date < CURDATE() + INTERVAL 7 DAY
    """)
    scheduled_maintenances = cursor.fetchone()[0]

    # Average flight distance
    cursor.execute("""
        SELECT AVG(distance) AS average_flight_distance
        FROM flights
    """)
    average_flight_distance = "{:.2f}".format(cursor.fetchone()[0])

    # Average flight time
    cursor.execute("""
        SELECT AVG(TIMESTAMPDIFF(MINUTE, scheduled_departure, scheduled_arrival)) AS average_flight_time
        FROM flights
    """)
    average_flight_time = "{:.2f}".format(cursor.fetchone()[0])

    # Most common aircraft types
    cursor.execute("""
        SELECT model, COUNT(*) AS count
        FROM aircrafts
        GROUP BY model
        ORDER BY count DESC
        LIMIT 1
    """)
    most_common_aircraft_types = cursor.fetchone()[0]

    connection.close()

    return render_template('dashboard.html', 
                           overall_avg_flights=overall_avg_flights, 
                           most_flown_aircraft=most_flown_aircraft, 
                           most_visited_airports=most_visited_airports, 
                           least_visited_airports=least_visited_airports, 
                           scheduled_maintenances=scheduled_maintenances, 
                           average_flight_distance=average_flight_distance, 
                           average_flight_time=average_flight_time, 
                           most_common_aircraft_types=most_common_aircraft_types)

@app.route('/airports')
def airports():
    search_params = {
        'icao_id': request.args.get('icao_id'),
        'civilian_name': request.args.get('civilian_name'),
        'latitude': request.args.get('latitude'),
        'longitude': request.args.get('longitude')
    }
    
    operators = {
        'icao_id': request.args.get('icao_id_operator', '='),
        'civilian_name': request.args.get('civilian_name_operator', '='),
        'latitude': request.args.get('latitude_operator', '='),
        'longitude': request.args.get('longitude_operator', '=')
    }
    
    query = "SELECT * FROM airports WHERE 1=1"
    params = []
    
    for field, value in search_params.items():
        if value:
            if operators[field] == "contains":
                query += f" AND `{field}` LIKE %s"
                params.append(f"%{value}%")
            else:
                query += f" AND `{field}` {operators[field]} %s"
                params.append(value)
    
    connection = mysql.connect()
    cursor = connection.cursor()
    cursor.execute(query, params)
    airport_list = cursor.fetchall()
    connection.close()
    
    return render_template('airports.html', airport_list=airport_list)

@app.route('/aircraft')
def aircraft():
    search_params = {
        'registration_code': request.args.get('registration_code'),
        'flight_range': request.args.get('flight_range'),
        'model': request.args.get('model'),
        'weight_capacity': request.args.get('weight_capacity'),
        'fuel_capacity': request.args.get('fuel_capacity'),
        'passenger_capacity': request.args.get('passenger_capacity'),
        'fuel_efficiency': request.args.get('fuel_efficiency'),
        'status': request.args.get('status'),
        'manufacturer': request.args.get('manufacturer'),
        'manufacture_date': request.args.get('manufacture_date'),
        'home_airport_id': request.args.get('home_airport'),
        'latest_arrival_airport_id': request.args.get('latest_airport')
    }
    
    operators = {
        'registration_code': request.args.get('registration_code_operator', '='),
        'flight_range': request.args.get('flight_range_operator', '='),
        'model': request.args.get('model_operator', '='),
        'weight_capacity': request.args.get('weight_capacity_operator', '='),
        'fuel_capacity': request.args.get('fuel_capacity_operator', '='),
        'passenger_capacity': request.args.get('passenger_capacity_operator', '='),
        'fuel_efficiency': request.args.get('fuel_efficiency_operator', '='),
        'status': request.args.get('status_operator', '='),
        'manufacturer': request.args.get('manufacturer_operator', '='),
        'manufacture_date': request.args.get('manufacture_date_operator', '='),
        'home_airport_id': request.args.get('home_airport_operator', '='),
        'latest_arrival_airport_id': request.args.get('latest_airport_operator', '=')
    }
    
    query = "SELECT * FROM aircrafts WHERE 1=1"
    params = []
    
    for field, value in search_params.items():
        if value:
            if operators[field] == "contains":
                query += f" AND `{field}` LIKE %s"
                params.append(f"%{value}%")
            else:
                query += f" AND `{field}` {operators[field]} %s"
                params.append(value)
    
    connection = mysql.connect()
    cursor = connection.cursor()
    cursor.execute(query, params)
    aircraft_list = cursor.fetchall()
    connection.close()
    
    return render_template('aircraft.html', aircraft_list=aircraft_list)

@app.route('/flights')
def flights():
    search_params = {
        'scheduled_departure': request.args.get('scheduled_departure'),
        'scheduled_arrival': request.args.get('scheduled_arrival'),
        'actual_departure': request.args.get('actual_departure'),
        'actual_arrival': request.args.get('actual_arrival'),
        'passenger_count': request.args.get('passenger_count'),
        'projected_fuel_consumption': request.args.get('projected_fuel_consumption'),
        'actual_fuel_consumption': request.args.get('actual_fuel_consumption'),
        'distance': request.args.get('distance'),
        'aircraft_id': request.args.get('aircraft_id'),
        'arrival_airport': request.args.get('arrival_airport'),
        'departure_airport': request.args.get('departure_airport')
    }
    
    operators = {
        'scheduled_departure': request.args.get('scheduled_departure_operator', '='),
        'scheduled_arrival': request.args.get('scheduled_arrival_operator', '='),
        'actual_departure': request.args.get('actual_departure_operator', '='),
        'actual_arrival': request.args.get('actual_arrival_operator', '='),
        'passenger_count': request.args.get('passenger_count_operator', '='),
        'projected_fuel_consumption': request.args.get('projected_fuel_consumption_operator', '='),
        'actual_fuel_consumption': request.args.get('actual_fuel_consumption_operator', '='),
        'distance': request.args.get('distance_operator', '='),
        'aircraft_id': request.args.get('aircraft_id_operator', '='),
        'arrival_airport': request.args.get('arrival_airport_operator', '='),
        'departure_airport': request.args.get('departure_airport_operator', '=')
    }
    
    query = "SELECT * FROM flights WHERE 1=1"
    params = []
    
    for field, value in search_params.items():
        if value:
            if operators[field] == "contains":
                query += f" AND `{field}` LIKE %s"
                params.append(f"%{value}%")
            else:
                query += f" AND `{field}` {operators[field]} %s"
                params.append(value)
    
    connection = mysql.connect()
    cursor = connection.cursor()
    cursor.execute(query, params)
    flight_list = cursor.fetchall()
    connection.close()
    
    return render_template('flights.html', flight_list=flight_list)

@app.route('/edit_airport/<icao_id>', methods=['GET', 'POST'])
def edit_airport(icao_id):
    if request.method == 'POST':
        # Process form data
        civilian_name = request.form['civilian_name']
        latitude = request.form['latitude']
        longitude = request.form['longitude']

        connection = mysql.connect()
        cursor = connection.cursor()
        cursor.execute("""
            UPDATE airports
            SET civilian_name = %s, latitude = %s, longitude = %s
            WHERE icao_id = %s
        """, (civilian_name, latitude, longitude, icao_id))
        connection.commit()
        connection.close()

        return redirect(url_for('app.airports'))

    connection = mysql.connect()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM airports WHERE icao_id = %s", (icao_id,))
    airport = cursor.fetchone()
    connection.close()
    return render_template('edit_airport.html', icao_id=icao_id, airport=airport)

@app.route('/edit_aircraft/<registration_code>', methods=['GET', 'POST'])
def edit_aircraft(registration_code):
    if request.method == 'POST':
        # Process form data
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

        connection = mysql.connect()
        cursor = connection.cursor()
        cursor.execute("""
            UPDATE aircrafts
            SET flight_range = %s, model = %s, weight_capacity = %s, fuel_capacity = %s, passenger_capacity = %s, fuel_efficiency = %s, status = %s, manufacturer = %s, manufacture_date = %s, home_airport_id = %s, latest_arrival_airport_id = %s
            WHERE registration_code = %s
        """, (flight_range, model, weight_capacity, fuel_capacity, passenger_capacity, fuel_efficiency, status, manufacturer, manufacture_date, home_airport_id, latest_arrival_airport_id, registration_code))
        connection.commit()
        connection.close()

        return redirect(url_for('app.aircraft'))

    connection = mysql.connect()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM aircrafts WHERE registration_code = %s", (registration_code,))
    aircraft = cursor.fetchone()
    connection.close()
    return render_template('edit_aircraft.html', registration_code=registration_code, aircraft=aircraft)

@app.route('/edit_flight/<flight_id>', methods=['GET', 'POST'])
def edit_flight(flight_id):
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
        arrival_airport = request.form['arrival_airport']
        departure_airport = request.form['departure_airport']

        connection = mysql.connect()
        cursor = connection.cursor()
        cursor.execute("""
            UPDATE flights
            SET scheduled_departure = %s, scheduled_arrival = %s, actual_departure = %s, actual_arrival = %s, passenger_count = %s, projected_fuel_consumption = %s, actual_fuel_consumption = %s, distance = %s, aircraft_id = %s, arrival_airport = %s, departure_airport = %s
            WHERE flight_id = %s
        """, (scheduled_departure, scheduled_arrival, actual_departure, actual_arrival, passenger_count, projected_fuel_consumption, actual_fuel_consumption, distance, aircraft_id, arrival_airport, departure_airport, flight_id))
        connection.commit()
        connection.close()

        return redirect(url_for('app.flights'))

    connection = mysql.connect()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM flights WHERE flight_id = %s", (flight_id,))
    flight = cursor.fetchone()
    connection.close()
    return render_template('edit_flight.html', flight_id=flight_id, flight=flight)

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