from flask import session, flash, redirect
from db import get_db_connection
from werkzeug.security import check_password_hash

def sign_in(email, password):
    conn = get_db_connection()
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
            print("Password mismatch")
    else:
        print("User not found")

    flash("Invalid email or password", "error")
    return redirect("/login")

def logout():
    session.clear()
