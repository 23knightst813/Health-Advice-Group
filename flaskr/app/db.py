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
