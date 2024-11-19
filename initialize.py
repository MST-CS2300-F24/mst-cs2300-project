import mysql.connector as mysql

def initialize():
    db = mysql.connect(
        host="localhost", # Change this to your MySQL host
        user="root", # Change this to your MySQL username
        passwd="admin" # Change this to your MySQL password
    )
    cursor = db.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS FlightOpsDb")
    cursor.execute("USE FlightOpsDb")
    cursor.execute("CREATE TABLE IF NOT EXISTS airports (icao_id VARCHAR(255) PRIMARY KEY, civilian_name VARCHAR(255), latitude FLOAT, longitude FLOAT)")
    cursor.execute("CREATE TABLE IF NOT EXISTS aircrafts (registration_code VARCHAR(255) PRIMARY KEY, flight_range FLOAT, model VARCHAR(255), weight_capacity FLOAT, fuel_capacity FLOAT, passenger_capacity INT, fuel_efficiency FLOAT, status VARCHAR(255), manufacturer VARCHAR(255), manufacture_date DATE, home_airport_id VARCHAR(255), latest_arrival_airport_id VARCHAR(255), FOREIGN KEY (home_airport_id) REFERENCES airports(icao_id), FOREIGN KEY (latest_arrival_airport_id) REFERENCES airports(icao_id))")
    cursor.execute("CREATE TABLE IF NOT EXISTS flights (flight_id INT AUTO_INCREMENT PRIMARY KEY, scheduled_departure DATETIME, scheduled_arrival DATETIME, actual_departure DATETIME, actual_arrival DATETIME, passenger_count INT, projected_fuel_consumption FLOAT, actual_fuel_consumption FLOAT, distance FLOAT, aircraft_id VARCHAR(255), origin_airport_id VARCHAR(255), destination_airport_id VARCHAR(255), FOREIGN KEY (aircraft_id) REFERENCES aircrafts(registration_code), FOREIGN KEY (origin_airport_id) REFERENCES airports(icao_id), FOREIGN KEY (destination_airport_id) REFERENCES airports(icao_id))")
    cursor.execute("CREATE TABLE IF NOT EXISTS maintenance_schedule (maintenance_id INT AUTO_INCREMENT PRIMARY KEY, suggested_maintenance_date DATE, maintenance_description VARCHAR(255), aircraft_id VARCHAR(255), maintenance_location_id VARCHAR(255), FOREIGN KEY (aircraft_id) REFERENCES aircrafts(registration_code), FOREIGN KEY (maintenance_location_id) REFERENCES airports(icao_id))")
    cursor.execute("CREATE TABLE IF NOT EXISTS maintenance_log (log_id INT AUTO_INCREMENT PRIMARY KEY, maintenance_start_date DATE, maintenance_end_date DATE, maintenance_description VARCHAR(255), aircraft_id VARCHAR(255), maintenance_location_id VARCHAR(255), FOREIGN KEY (aircraft_id) REFERENCES aircrafts(registration_code), FOREIGN KEY (maintenance_location_id) REFERENCES airports(icao_id))")

    db.commit()
    db.close()
    return

initialize()
