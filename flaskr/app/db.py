import sqlite3
from werkzeug.security import generate_password_hash
import time
import logging

def set_up_db():
    """
    Set up the database by creating necessary tables if they do not exist.
    """
    conn = sqlite3.connect('Health.db')
    cursor = conn.cursor()
    
    # Create users table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT NOT NULL UNIQUE,
        password_hash TEXT NOT NULL,
        crd TEXT DEFAULT NONE, 
        is_admin BOOLEAN DEFAULT FALSE,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    # Create risk_assessments table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS risk_assessments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        postcode TEXT NOT NULL,
        indoor_temp REAL NOT NULL,
        indoor_humidity REAL NOT NULL,
        smoke_detectors INTEGER NOT NULL,
        co_alarms INTEGER NOT NULL,
        assessment_type TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users (id)
    )
    ''')
    
    # Create bookings table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS bookings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        assessment_id INTEGER NOT NULL,
        name TEXT NOT NULL,
        email TEXT NOT NULL,
        phone TEXT NOT NULL,
        address TEXT NOT NULL,
        date TEXT NOT NULL,
        time TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users (id),
        FOREIGN KEY (assessment_id) REFERENCES risk_assessments (id)
    )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS symptom_tracker (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            severity INTEGER CHECK (severity BETWEEN 0 AND 5),
            mood TEXT CHECK (mood IN ('Sad', 'Neutral', 'Happy')),
            temperature REAL,
            humidity REAL,
            wind_speed REAL,
            weather_condition TEXT,
            air_quality_index INTEGER,
            air_quality_status TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    conn.commit()
    conn.close()



def add_user(email, password, CRD):
    """
    Add a new user to the database with retry logic for locked database.
    
    Args:
        email (str): The email address of the user.
        password (str): The password provided by the user.
        CRD (str): The chronic respiratory disease of the user.
    
    Returns:
        bool: True if the user was added successfully, False if the user already exists.
    """
    max_attempts = 3  # Maximum number of attempts to try inserting the user
    attempt = 0  # Current attempt count
    
    while attempt < max_attempts:
        try:
            # Connect to the database with a timeout to handle locked database
            conn = sqlite3.connect('Health.db', timeout=20)
            cursor = conn.cursor()
            hashed_password = generate_password_hash(password)  # Hash the user's password
            
            # Insert the new user into the users table
            cursor.execute('''
                INSERT INTO users (email, password_hash, crd)
                VALUES (?, ?, ?)
            ''', (email, hashed_password, CRD))
            
            conn.commit()  # Commit the transaction
            logging.info('User added successfully!')  # Log success message
            return True
            
        except sqlite3.IntegrityError:
            # Handle case where the user already exists
            logging.error('User already exists!')  # Log error message
            return False
            
        except sqlite3.OperationalError as e:
            # Handle operational errors such as database being locked
            if "database is locked" in str(e):
                attempt += 1  # Increment the attempt count
                if attempt < max_attempts:
                    logging.warning('Database is locked, retrying...')  # Log warning message
                    time.sleep(1)  # Wait before retrying
                    continue
            raise  # Re-raise the exception if it's not a locked database error
            
        finally:
            if 'conn' in locals():
                conn.close()  # Ensure the database connection is closed
    
    logging.error('Failed to add user after multiple attempts.')  # Log error message if all attempts fail
    return False

def save_risk_assessment(user_id, postcode, indoor_temp, indoor_humidity, smoke_detectors, co_alarms, assessment_type):
    """
    Save a risk assessment to the database.
    
    Args:
        user_id (int): The ID of the user.
        postcode (str): The postcode of the user's location.
        indoor_temp (float): The indoor temperature.
        indoor_humidity (float): The indoor humidity.
        smoke_detectors (int): The number of smoke detectors.
        co_alarms (int): The number of carbon monoxide alarms.
        assessment_type (str): The type of assessment (e.g., "human" or "ai").
    """
    conn = sqlite3.connect('Health.db')
    cursor = conn.cursor()
    # Insert risk assessment into the risk_assessments table
    cursor.execute('''
        INSERT INTO risk_assessments (user_id, postcode, indoor_temp, indoor_humidity, smoke_detectors, co_alarms, assessment_type)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (user_id, postcode, indoor_temp, indoor_humidity, smoke_detectors, co_alarms, assessment_type))
    conn.commit()
    conn.close()

def get_latest_assessment_id(user_id):
    """
    Get the ID of the latest risk assessment for a user.
    
    Args:
        user_id (int): The ID of the user.
    
    Returns:
        int: The ID of the latest risk assessment, or None if no assessments are found.
    """
    conn = sqlite3.connect('Health.db')
    cursor = conn.cursor()
    # Select the latest risk assessment ID for the user
    cursor.execute('''
        SELECT id FROM risk_assessments WHERE user_id = ? ORDER BY created_at DESC LIMIT 1
    ''', (user_id,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else None

def save_booking(user_id, assessment_id, name, email, phone, address, date, time):
    """
    Save a booking to the database.
    
    Args:
        user_id (int): The ID of the user.
        assessment_id (int): The ID of the risk assessment.
        name (str): The name of the person booking the assessment.
        email (str): The email address of the person booking the assessment.
        phone (str): The phone number of the person booking the assessment.
        address (str): The address of the person booking the assessment.
        date (str): The date of the booking.
        time (str): The time of the booking.
    """
    conn = sqlite3.connect('Health.db')
    cursor = conn.cursor()
    # Insert booking into the bookings table
    cursor.execute('''
        INSERT INTO bookings (user_id, assessment_id, name, email, phone, address, date, time)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (user_id, assessment_id, name, email, phone, address, date, time))
    conn.commit()
    conn.close()


def save_symptom_record(user_id, severity, mood, temperature, humidity, wind_speed, weather_condition, air_quality_index, air_quality_status):
    """Save a symptom tracking record to the database."""
    conn = sqlite3.connect('Health.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO symptom_tracker 
        (user_id, severity, mood, temperature, humidity, wind_speed, weather_condition, 
         air_quality_index, air_quality_status)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (user_id, severity, mood, temperature, humidity, wind_speed, weather_condition,
          air_quality_index, air_quality_status))
    conn.commit()
    conn.close()

def get_symptom_history_labels(user_id):
    """Get dates for symptom history chart."""
    conn = sqlite3.connect('Health.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT created_at FROM symptom_tracker 
        WHERE user_id = ? 
        ORDER BY created_at DESC LIMIT 7
    ''', (user_id,))
    dates = cursor.fetchall()
    conn.close()
    return [date[0].split()[0] for date in dates][::-1]

def get_symptom_history_data(user_id):
    """Get severity values for symptom history chart."""
    conn = sqlite3.connect('Health.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT severity FROM symptom_tracker 
        WHERE user_id = ? 
        ORDER BY created_at DESC LIMIT 7
    ''', (user_id,))
    severity = cursor.fetchall()
    conn.close()
    return [s[0] for s in severity][::-1]
