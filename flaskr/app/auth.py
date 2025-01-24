# auth.py
# Purpose: Handles user authentication, including sign-in and logout functionality
# Author: Theo
# Date: 28 November 2024
# Notes: Implements password hashing for secure authentication.

# Import necessary modules from Flask and other libraries
import sqlite3
from flask import session, flash, redirect
from db import get_db_connection
from werkzeug.security import check_password_hash

# Function to get the user ID based on the provided email
def get_user_id_by_email(email):
    """
    Get the user ID based on the provided email.

    Parameters:
        email (str): The email of the user.

    Returns:
        int: The user ID if found, None otherwise.

    Raises:
        None
    """
    # Connect to the SQLite database 'dojo.db'
    conn = sqlite3.connect('dojo.db')
    # Create a cursor object to interact with the database
    cursor = conn.cursor()
    # Execute a query to fetch the user ID based on the provided email
    cursor.execute('SELECT user_id FROM users WHERE email = ?', (email,))
    # Fetch the result from the query
    result = cursor.fetchone()
    # Close the database connection
    conn.close()
    # Return the user ID if found, otherwise return None
    return result[0] if result else None

# Function to authenticate a user by validating their credentials
def sign_in(email, password):
    """
    Authenticate a user by validating their credentials.

    Parameters:
        email (str): The email of the user.
        password (str): The plain-text password provided by the user.

    Returns:
        Response: Redirect to the appropriate page based on the authentication outcome.

    Raises:
        None
    """
    conn = get_db_connection()  # Get a connection to the database
    cur = conn.cursor()  # Create a cursor object to interact with the database
    query = """SELECT email, password, is_admin FROM users WHERE email = ?"""
    cur.execute(query, (email,))  # Execute the query to fetch user data based on the provided email
    user = cur.fetchone()  # Fetch the first result from the query
    conn.close()  # Close the database connection

    if user:
        print(f"User found: {user[0]}, Hashed Password: {user[1]}")  # Debug statement
        if check_password_hash(user[1], password):  # Check if user exists and password is correct
            session["email"] = user[0]  # Store the user's email in the session
            session["is_admin"] = bool(user[2])  # Store the user's admin status in the session
            if session["is_admin"]:  # If the user is an admin, redirect to the admin page
                return redirect("/admin")
            return redirect("/")  # Otherwise, redirect to the home page
        else:
            print("Password mismatch")  # Debug statement
    else:
        print("User not found")  # Debug statement

    flash("Invalid email or password", "error")  # Display an error message if authentication fails
    return redirect("/login")  # Redirect to the login page

# Function to clear the user session to log out the user
def logout():
    """
    Clear the user session to log out the user.

    Returns:
        None
    """
    session.clear()  # Clear all data from the session