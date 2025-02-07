from flask import Flask, render_template, request, flash, redirect, session , url_for

from db import set_up_db,  add_user, save_risk_assessment,  get_latest_assessment_id, save_booking
from auth import sign_in, get_user_id_by_email
from validation import is_not_empty, is_valid_email, is_secure_password
from weather import  get_weather_data ,  get_air_ai_tips , get_aqi_category, get_ai_assesment_tips


app = Flask(__name__, static_folder='../static')


app.secret_key = 'secret_key' 



@app.route("/")
def index():
    """
    Render the home page of the application.
    """
    return render_template('index.html')

@app.route("/logout")
def logout():
    """
    Clear the user session and redirect to the home page.
    """
    session.clear()
    return redirect("/")

@app.route("/register", methods=["GET", "POST"])
def register():
    """
    Handle user registration. Validate input, check for existing account, and add new user to the database.
    """
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        password2 = request.form["password2"]
        CRD = request.form["CRD"]

        # Validate input fields
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

        # Add user to the database
        if not add_user(email, password, CRD):
            flash("Account already exists", "error")
            return redirect("/register")
        flash("Registration successful.", "success")
        sign_in(email, password)
        return redirect("/")
    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    """
    Handle user login. Validate input and authenticate user.
    """
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        return sign_in(email, password)

    return render_template("login.html")

@app.route("/forecast")
def forecast():
    """
    Render the weather forecast page with data.
    """
    data = get_weather_data()

    if not data:
        flash("Unable to retrieve weather forecast.", "error")
        return render_template("forecast.html", data=None)

    return render_template("forecast.html", data=data)

@app.route("/dashboard")
def dashboard():
    """
    Render the dashboard page with air quality data and recommendations.
    """
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

@app.route("/risk_assessment", methods=["GET", "POST"])
def risk_assessment():
    """
    Handle risk assessment form submission. Save data to the database and redirect based on assessment type.
    """
    if "email" not in session:
        flash("You must be signed in to perform a risk assessment", "error")
        return redirect(url_for("login"))

    if request.method == "POST":
        postcode = request.form.get("postcode")
        indoor_temp = request.form.get("indoor_temp")
        indoor_humidity = request.form.get("indoor_humidity")
        smoke_detectors = request.form.get("smoke_detectors")
        co_alarms = request.form.get("co_alarms")
        assessment_type = request.form.get("assessment_type")

        if not all([postcode, indoor_temp, indoor_humidity, smoke_detectors, co_alarms, assessment_type]):
            flash("All fields are required", "error")
            return redirect(url_for("dashboard"))
        
        user_id = get_user_id_by_email()
        # Save data to database
        save_risk_assessment(user_id, postcode, indoor_temp, indoor_humidity, smoke_detectors, co_alarms, assessment_type)

        flash("Risk Assessment submitted!", "success")
        if assessment_type == "human":
            return redirect("/assessment_booking")
        if assessment_type == "ai":
            return redirect("/ai_assessment")

    return render_template("risk_assessment.html")

@app.route("/ai_assessment", methods=["GET", "POST"])
def ai_assessment():
    """
    Render the AI-powered risk assessment page with AI-generated tips.
    """
    ai_tips = get_ai_assesment_tips()
    return render_template("ai_assessment.html", ai_tips=ai_tips)

@app.route("/assessment_booking", methods=["GET", "POST"])
def assessment_booking():
    """
    Handle assessment booking form submission. Save booking data to the database.
    """
    if request.method == "POST":
        # Get form data
        name = request.form.get("name")
        email = request.form.get("email")
        phone = request.form.get("phone")
        address = request.form.get("address")
        date = request.form.get("date")
        time = request.form.get("time")

        user_id = get_user_id_by_email()

        assessment_id = get_latest_assessment_id(user_id)

        if not all([name, email, phone, address, date, time]):
            flash("All fields are required", "error")
            return redirect(url_for("assessment_booking"))

        # Save booking data to the database (assuming a function save_booking exists)
        save_booking(user_id ,assessment_id, name, email, phone, address, date, time)

        flash("Assessment booked successfully!", "success")
        return redirect(url_for("index"))
            
    return render_template("assessment_booking.html")


if __name__ == "__main__":
    set_up_db()
    app.run(debug=True) 
