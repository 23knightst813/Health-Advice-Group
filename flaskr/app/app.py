from flask import Flask, render_template, request, flash, redirect, session

from db import set_up_db,  add_user
from auth import sign_in
from validation import is_not_empty, is_valid_email, is_secure_password
from weather import  get_weather_data ,  get_air_ai_tips


app = Flask(__name__, static_folder='../static')


app.secret_key = 'secret_key' 

def get_aqi_category(aqi):
    """Categorize AQI value into quality groups."""
    aqi = int(aqi)
    if aqi <= 50: return 'good'
    elif aqi <= 100: return 'moderate'
    elif aqi <= 150: return 'unhealthy-sensitive'
    elif aqi <= 200: return 'unhealthy'
    elif aqi <= 300: return 'very-unhealthy'
    else: return 'hazardous'

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
    """Enhanced dashboard route with dynamic data handling."""
    dashboard_data = {
        'AQI': '',
        'summary': 'Data not available',
        'recommendations': 'Check back later',
        'category': 'moderate',
        'error': None
    }

    if not session.get("user"):
        flash("Login for personalized recommendations", "warning")

    try:
        ai_data = get_air_ai_tips() or {}
        dashboard_data.update(ai_data)
        
        if 'AQI' in ai_data:
            dashboard_data['category'] = get_aqi_category(int(ai_data['AQI']))
            
    except Exception as e:
        flash(f"Dashboard error: {str(e)}", "error")
        dashboard_data['error'] = "Unable to load air quality data"

    return render_template("dashboard.html", data=dashboard_data)


if __name__ == "__main__":
    set_up_db()
    app.run(debug=True)