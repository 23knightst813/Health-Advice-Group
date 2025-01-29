import sqlite3
from werkzeug.security import generate_password_hash

def get_db_connection():
    # Return a connection to the SQLite database 'dojo.db'
    return sqlite3.connect('Health.db')

def set_up_db():
    conn = get_db_connection()
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
    conn.commit()
    conn.close()


def add_user(email, password, CRD):
    conn = get_db_connection()
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