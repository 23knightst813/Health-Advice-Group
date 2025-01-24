# db.py
# Purpose: Handles database setup and operations for the Coder Dojo web application
# Author: Theo
# Date: 28 November 2024
# Notes: Implements database schema creation and user management functions.

# Import the sqlite3 module for database operations
import sqlite3
# Import the generate_password_hash function from werkzeug.security for password hashing
from werkzeug.security import generate_password_hash

import sqlite3
from werkzeug.security import generate_password_hash


def setup_db():
    """
    Set up the database for the Health Advice project with descriptive IDs
    and proper foreign key relationships
    """
    # Connect to SQLite database
    conn = sqlite3.connect('health.db')
    cursor = conn.cursor()
    
    # Enable foreign key constraints
    cursor.execute('PRAGMA foreign_keys = ON;')

    # Create Users table 
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            is_admin BOOLEAN DEFAULT FALSE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )''')

    # Create Locations table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS locations (
            location_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            city TEXT NOT NULL,
            country TEXT NOT NULL,
            latitude DECIMAL(9,6) NOT NULL,
            longitude DECIMAL(9,6) NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(user_id)
        )''')

    # Create Weather Data table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS weather_data (
            weather_id INTEGER PRIMARY KEY AUTOINCREMENT,
            location_id INTEGER NOT NULL,
            temperature DECIMAL(5,2) NOT NULL,
            humidity INTEGER NOT NULL,
            wind_speed DECIMAL(5,2) NOT NULL,
            weather_condition TEXT NOT NULL,  -- Renamed from 'condition'
            forecast_time TIMESTAMP NOT NULL,
            FOREIGN KEY (location_id) REFERENCES locations(location_id)
        )''')

    # Create Air Quality Data table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS air_quality_data (
            air_quality_id INTEGER PRIMARY KEY AUTOINCREMENT,
            location_id INTEGER NOT NULL,
            aqi INTEGER NOT NULL,
            pm25 DECIMAL(5,2) NOT NULL,
            pm10 DECIMAL(5,2) NOT NULL,
            no2 DECIMAL(5,2) NOT NULL,
            co DECIMAL(5,2) NOT NULL,
            so2 DECIMAL(5,2) NOT NULL,
            o3 DECIMAL(5,2) NOT NULL,
            measurement_time TIMESTAMP NOT NULL,
            FOREIGN KEY (location_id) REFERENCES locations(location_id)
        )''')

    # Create Health Tracking table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS health_tracking (
            tracking_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            symptom TEXT NOT NULL,
            severity INTEGER NOT NULL,
            notes TEXT,
            log_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(user_id)
        )''')

    # Create Risk Assessments tables
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS assessments (
            assessment_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            assessment_type TEXT NOT NULL,
            risk_level TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            assessment_result TEXT,
            human_assessment_required BOOLEAN DEFAULT FALSE,
            FOREIGN KEY (user_id) REFERENCES users(user_id)
        )''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS inputs (
            input_id INTEGER PRIMARY KEY AUTOINCREMENT,
            assessment_id INTEGER NOT NULL,
            indoor_temp REAL,
            indoor_humidity REAL,
            allergy_triggers BOOLEAN,
            ventilation_quality INTEGER,
            fire_alarm_count INTEGER,
            carbon_monoxide_alarm_count INTEGER,
            FOREIGN KEY (assessment_id) REFERENCES assessments(assessment_id)
        )''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS appointments (
            appointment_id INTEGER PRIMARY KEY AUTOINCREMENT,
            assessment_id INTEGER NOT NULL,
            address TEXT NOT NULL,
            appointment_date DATE NOT NULL,
            appointment_time TIME NOT NULL,
            confirmed BOOLEAN DEFAULT FALSE,
            FOREIGN KEY (assessment_id) REFERENCES assessments(assessment_id)
        )''')

    # Create Accessibility Preferences table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS accessibility_preferences (
            preference_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            preference_type TEXT NOT NULL,
            preference_value TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(user_id)
        )''')

    # Create Admin account with proper columns
    admin_password = generate_password_hash('adminpass')
    cursor.execute('''
        INSERT OR IGNORE INTO users 
        (email, password, first_name, last_name, is_admin)
        VALUES (?, ?, ?, ?, TRUE)
    ''', (
        'admin@healthadvice.org',
        admin_password,
        'System',
        'Administrator'
    ))

    # Commit changes and close connection
    conn.commit()
    conn.close()


# Function to add a new user to the database
def add_user(email, password, first_name, last_name):
    """
    Add a new user to the database.

    Parameters:
        email (str): The email of the user.
        password (str): The plain-text password provided by the user.
        first_name (str): The first name of the user.
        last_name (str): The last name of the user.

    Returns:
        bool: True if the user is added successfully, False otherwise.

    Raises:
        None
    """
    # Connect to the SQLite database 'dojo.db'
    conn = sqlite3.connect('dojo.db')
    # Create a cursor object to interact with the database
    cursor = conn.cursor()
    # Hash the plain-text password
    hashed_password = generate_password_hash(password)
    try:
        # Insert the new user into the 'users' table
        cursor.execute('''
            INSERT INTO users (email, password, first_name, last_name)
            VALUES (?, ?, ?, ?)
        ''', (email, hashed_password, first_name, last_name))
        # Commit the changes to the database
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        # Close the database connection
        conn.close()



# Function to get a connection to the database
def get_db_connection():
    """
    Get a connection to the database.

    Returns:
        Connection: A SQLite database connection.

    Raises:
        None
    """
    # Return a connection to the SQLite database 'dojo.db'
    return sqlite3.connect('flaskr/app/health.db')

if __name__ == '__main__':
    setup_db()
    print("Database setup completed successfully.")