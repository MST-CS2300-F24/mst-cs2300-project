from flask import Blueprint, jsonify, request
from mysql.connector import connect
from datetime import datetime, timedelta

# Create a new blueprint for performance reports
reports_blueprint = Blueprint('reports', __name__)

# Database connection function
def get_db_connection():
    return connect(
        host="localhost",
        user="root",
        password="admin",  # Change to your MySQL password
        database="FlightOpsDb"
    )

@reports_blueprint.route('/performance', methods=['GET'])
def generate_performance_report():
    try:
        # Retrieve parameters from the request
        aircraft_id = request.args.get('aircraft_id')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')

        # Validate parameters
        if not aircraft_id or not start_date or not end_date:
            return jsonify({"error": "Missing required parameters"}), 400

        start_date = datetime.strptime(start_date, "%Y-%m-%d")
        end_date = datetime.strptime(end_date, "%Y-%m-%d")

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        # Total distance traveled
        cursor.execute("""
            SELECT SUM(distance) AS total_distance
            FROM flights
            WHERE aircraft_id = %s AND scheduled_departure_datetime BETWEEN %s AND %s
        """, (aircraft_id, start_date, end_date))
        total_distance = cursor.fetchone()['total_distance'] or 0

        # Total fuel consumed
        cursor.execute("""
            SELECT SUM(actual_fuel_consumption) AS total_fuel
            FROM flights
            WHERE aircraft_id = %s AND scheduled_departure_datetime BETWEEN %s AND %s
        """, (aircraft_id, start_date, end_date))
        total_fuel = cursor.fetchone()['total_fuel'] or 0

        # Utilization percentage
        cursor.execute("""
            SELECT AVG(passenger_count / passenger_capacity) * 100 AS utilization_percentage
            FROM flights
            JOIN aircrafts ON flights.aircraft_id = aircrafts.registration_code
            WHERE aircraft_id = %s AND scheduled_departure_datetime BETWEEN %s AND %s
        """, (aircraft_id, start_date, end_date))
        utilization_percentage = cursor.fetchone()['utilization_percentage'] or 0

        # Suggested maintenance date
        cursor.execute("""
            SELECT MIN(suggested_date) AS next_maintenance_date
            FROM maintenance_schedule
            WHERE aircraft_id = %s AND suggested_date > %s
        """, (aircraft_id, datetime.now()))
        next_maintenance_date = cursor.fetchone()['next_maintenance_date']

        # Last serviced date
        cursor.execute("""
            SELECT MAX(service_finish) AS last_serviced_date
            FROM maintenance_history
            WHERE aircraft_id = %s
        """, (aircraft_id,))
        last_serviced_date = cursor.fetchone()['last_serviced_date']

        # Flights per month for the last 12 months
        cursor.execute("""
            SELECT YEAR(scheduled_departure_datetime) AS year,
                   MONTH(scheduled_departure_datetime) AS month,
                   COUNT(*) AS flights_count
            FROM flights
            WHERE aircraft_id = %s AND scheduled_departure_datetime >= %s
            GROUP BY year, month
            ORDER BY year, month
        """, (aircraft_id, datetime.now() - timedelta(days=365)))
        flights_per_month = cursor.fetchall()

        conn.close()

        # Build the report
        report = {
            "aircraft_id": aircraft_id,
            "total_distance_traveled": total_distance,
            "total_fuel_consumed": total_fuel,
            "utilization_percentage": utilization_percentage,
            "next_maintenance_date": next_maintenance_date,
            "last_serviced_date": last_serviced_date,
            "flights_per_month": flights_per_month
        }
        return jsonify(report)

    except Exception as e:
        return jsonify({"error": str(e)}), 500
