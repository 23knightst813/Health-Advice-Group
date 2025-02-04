from flask import Flask, render_template, request, flash, redirect, session

from db import set_up_db,  add_user
from auth import sign_in
from validation import is_not_empty, is_valid_email, is_secure_password
from weather import  get_weather_data


app = Flask(__name__, static_folder='../static')


app.secret_key = 'secret_key' 

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        password2 = request.form["password2"]
        CRD = request.form["CRD"]

        if not all([is_not_empty(email), is_not_empty(password)]):
            flash("All fields are required", "error")
            return redirect("/register")

        if not is_valid_email(email):
            flash("Invalid email address", "error")
            return redirect("/register")

        if password != password2:
            flash("Passwords do not match", "error")
            return redirect("/register")

        if not is_secure_password(password):
            flash(
                "Password must be at least 8 characters long, contain an uppercase letter, a lowercase letter, a number, and a special character.",
                "error"
            )
            return redirect("/register")

        if not add_user(email, password, CRD):
            flash("Account already exists", "error")
            return redirect("/register")
        flash("Registration successful.", "success")
        sign_in(email, password)
        return redirect("/")
    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        return sign_in(email, password)

    return render_template("login.html")

@app.route("/forecast")
def forecast():
    """Flask route for weather forecast page."""
    data = get_weather_data()

    if not data:
        flash("Unable to retrieve weather forecast.", "error")
        return render_template("forecast.html", data=None)

    return render_template("forecast.html", data=data)

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")



if __name__ == "__main__":
    set_up_db()
    app.run(debug=True)