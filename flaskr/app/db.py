import sqlite3
from werkzeug.security import generate_password_hash

def get_db_connection():
    # Return a connection to the SQLite database 'dojo.db'
    return sqlite3.connect('Health.db')

def set_up_db():

    conn  = get_db_connection()
    cursor = conn.cursor()
    
    # Create the 'users' table if it doesn't exist
    cursor.execute('''
    CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    crd TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    ''')


set_up_db()