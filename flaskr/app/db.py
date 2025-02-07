import sqlite3
from werkzeug.security import generate_password_hash




def set_up_db():
    conn = sqlite3.connect('Health.db')
    cursor = conn.cursor()
    
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
    
    conn.commit()
    conn.close()

def add_user(email, password, CRD):
    conn = sqlite3.connect('Health.db')
    cursor = conn.cursor()
    hashed_password = generate_password_hash(password)
    try:
        # Correct the SQL syntax and column names
        cursor.execute('''
            INSERT INTO users (email, password_hash, crd)
            VALUES (?, ?, ?)
        ''', (email, hashed_password, CRD))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def save_risk_assessment(user_id ,postcode, indoor_temp, indoor_humidity, smoke_detectors, co_alarms, assessment_type):
    conn = sqlite3.connect('Health.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO risk_assessments (user_id, postcode, indoor_temp, indoor_humidity, smoke_detectors, co_alarms, assessment_type)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (user_id, postcode, indoor_temp, indoor_humidity, smoke_detectors, co_alarms, assessment_type))
    conn.commit()
    conn.close()

def get_latest_assessment_id(user_id):
    conn = sqlite3.connect('Health.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT id FROM risk_assessments WHERE user_id = ? ORDER BY created_at DESC LIMIT 1
    ''', (user_id,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else None

def  save_booking(user_id ,assessment_id, name, email, phone, address, date, time):
    conn = sqlite3.connect('Health.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO bookings (user_id, assessment_id, name, email, phone, address, date, time)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (user_id ,assessment_id, name, email, phone, address, date, time))
    conn.commit()
    conn.close()
