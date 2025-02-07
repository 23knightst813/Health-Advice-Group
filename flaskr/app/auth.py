from flask import session, flash, redirect
import sqlite3
from werkzeug.security import check_password_hash

def sign_in(email, password):
    """
    Authenticate a user by checking their email and password against the database.
    
    Args:
        email (str): The email address of the user.
        password (str): The password provided by the user.
    
    Returns:
        redirect: Redirects to the appropriate page based on authentication success.
    """
    conn = sqlite3.connect('Health.db')
    cur = conn.cursor()
    query = """SELECT email, password_hash, is_admin FROM users WHERE email = ?"""
    cur.execute(query, (email,))
    user = cur.fetchone()
    conn.close()

    if user:
        print(f"User found: {user[0]}, Hashed Password: {user[1]}")
        if check_password_hash(user[1], password):
            session["email"] = user[0]
            session["is_admin"] = bool(user[2])
            if session["is_admin"]:
                return redirect("/admin")
            return redirect("/")
        else:
            flash("Invalid password", "error")
    else:
        flash("User not found", "error")

    flash("Invalid email or password", "error")
    return redirect("/login")

def get_user_id_by_email():
    """
    Retrieve the user ID based on the email stored in the session.
    
    Returns:
        int: The user ID if found, otherwise None.
    """
    try:
        email = session.get("email")
        if not email:
            flash("User not logged in", "error")
            return None
            
        conn = sqlite3.connect('Health.db')
        cursor = conn.cursor()
        cursor.execute('SELECT id FROM users WHERE email = ?', (email,))
        result = cursor.fetchone()
        conn.close()
        
        if not result:
            flash("User not found", "error")
            return None
            
        return result[0]
    except Exception as e:
        flash(f"Database error: {str(e)}", "error")
        return None
