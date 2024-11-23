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

# Additional route for performance reports
@app.route('/performance_report')
def performance_report():
    try:
        # Get parameters from the request
        aircraft_id = request.args.get('aircraft_id')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')

        # Validate input
        if not aircraft_id or not start_date or not end_date:
            flash("Missing parameters! Please provide aircraft_id, start_date, and end_date.", "error")
            return redirect(url_for('app.home'))

        connection = mysql.connect()
        cursor = connection.cursor(dictionary=True)

        # Total distance traveled
        cursor.execute("""
            SELECT SUM(distance) AS total_distance
            FROM flights
            WHERE aircraft_id = %s AND scheduled_departure >= %s AND scheduled_departure <= %s
        """, (aircraft_id, start_date, end_date))
        total_distance = cursor.fetchone()['total_distance'] or 0

        # Total fuel consumed
        cursor.execute("""
            SELECT SUM(actual_fuel_consumption) AS total_fuel
            FROM flights
            WHERE aircraft_id = %s AND scheduled_departure >= %s AND scheduled_departure <= %s
        """, (aircraft_id, start_date, end_date))
        total_fuel = cursor.fetchone()['total_fuel'] or 0

        # Utilization percentage
        cursor.execute("""
            SELECT AVG(passenger_count / passenger_capacity) * 100 AS utilization
            FROM flights
            JOIN aircrafts ON flights.aircraft_id = aircrafts.registration_code
            WHERE aircraft_id = %s AND scheduled_departure >= %s AND scheduled_departure <= %s
        """, (aircraft_id, start_date, end_date))
        utilization = cursor.fetchone()['utilization'] or 0

        # Next maintenance date
        cursor.execute("""
            SELECT MIN(suggested_date) AS next_maintenance
            FROM maintenance_schedule
            WHERE aircraft_id = %s AND suggested_date >= CURDATE()
        """, (aircraft_id,))
        next_maintenance = cursor.fetchone()['next_maintenance']

        # Last serviced date
        cursor.execute("""
            SELECT MAX(service_finish) AS last_serviced
            FROM maintenance_log
            WHERE aircraft_id = %s
        """, (aircraft_id,))
        last_serviced = cursor.fetchone()['last_serviced']

        # Flights per month for the past 12 months
        cursor.execute("""
            SELECT YEAR(scheduled_departure) AS year, MONTH(scheduled_departure) AS month, COUNT(*) AS flight_count
            FROM flights
            WHERE aircraft_id = %s AND scheduled_departure >= CURDATE() - INTERVAL 1 YEAR
            GROUP BY year, month
            ORDER BY year, month
        """, (aircraft_id,))
        flights_per_month = cursor.fetchall()

        connection.close()

        # Pass the data to the template
        return render_template('performance_report.html', 
                               aircraft_id=aircraft_id,
                               total_distance=total_distance,
                               total_fuel=total_fuel,
                               utilization=utilization,
                               next_maintenance=next_maintenance,
                               last_serviced=last_serviced,
                               flights_per_month=flights_per_month)

    except Exception as e:
        flash(f"Error generating report: {e}", "error")
        return redirect(url_for('app.home'))
