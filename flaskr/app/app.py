import logging
from flask import Flask, render_template, request, flash, redirect, session, url_for, jsonify


from db import set_up_db,  add_user, save_risk_assessment,  get_latest_assessment_id, save_booking, save_symptom_record, get_symptom_history_labels, get_symptom_history_data
from auth import sign_in, get_user_id_by_email
from validation import is_not_empty, is_valid_email, is_secure_password
from weather import  get_weather_data ,  get_air_ai_tips , get_aqi_category, get_ai_assesment_tips, get_air_quality, get_tacker_weather_data
from RateLimit import rate_limit

app = Flask(__name__, static_folder='../static')


app.secret_key = 'secret_key' 

@app.route("/set_user_ip", methods=["POST"])
def set_user_ip():
    """
    Set the user's IP address in the session.
    """
    try:
        user_ip = request.json.get('ip')
        session['user_ip'] = user_ip
        print(user_ip)
        return jsonify({"success": True}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


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
@rate_limit()
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
@rate_limit()
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
@rate_limit()
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
@rate_limit()
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
@rate_limit()
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
@rate_limit()
def ai_assessment():
    """
    Render the AI-powered risk assessment page with AI-generated tips.
    """
    ai_tips = get_ai_assesment_tips()
    return render_template("ai_assessment.html", ai_tips=ai_tips)

@app.route("/assessment_booking", methods=["GET", "POST"])
@rate_limit()
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


@app.route('/tracker')
def tracker():
    """
    Handle symptom tracking functionality. Retrieves weather, air quality, and symptom history data.
    """
    if "email" not in session:
        flash("You must be signed in to use the tracker", "error")
        return redirect(url_for("login"))
        
    user_id = get_user_id_by_email()
    
    # Get weather and air quality data
    weather_data = get_tacker_weather_data()
    if not weather_data:
        flash("Unable to retrieve weather data", "error")
        return render_template("tracker.html", data={
            'symptom_labels': [],
            'symptom_data': [],
            'air_quality': {'index': 0, 'status': 'Unknown'},
            'weather': {
                'temperature': 0,
                'condition': 'Unknown',
                'humidity': 0,
                'wind_speed': 0
            }
        })

    air_quality_data = get_air_quality()
    air_quality_index = air_quality_data['aqi']
    # Get air quality category
    aqi_category = get_aqi_category(air_quality_index)
    
    # Format data for template
    data = {
        'symptom_labels': get_symptom_history_labels(user_id),
        'symptom_data': get_symptom_history_data(user_id),
        'air_quality': {
            'index': air_quality_index,
            'status': aqi_category
        },
        'weather': {
            'temperature': weather_data['temperature'],
            'condition': weather_data['condition'],
            'humidity': weather_data['humidity'],
            'wind_speed': weather_data['wind_speed']
        }
    }
    
    return render_template('tracker.html',
                         symptom_labels=data['symptom_labels'],
                         symptom_data=data['symptom_data'],
                         air_quality_index=round(data['air_quality']['index']),
                         air_quality_status=data['air_quality']['status'],
                         temperature=data['weather']['temperature'],
                         condition=data['weather']['condition'],
                         humidity=data['weather']['humidity'],
                         wind_speed=data['weather']['wind_speed'])


@app.route('/log_mood', methods=['POST'])
@rate_limit()
def log_mood():
    """
    Handle mood logging from the symptom tracker.
    """
    if "email" not in session:
        flash("Please login to track your symptoms", "error")
        return {"error": "Not logged in"}, 401

    mood = request.json.get('mood')
    if mood not in ['Sad', 'Neutral', 'Happy']:
        flash("Invalid mood selection", "error")
        return {"error": "Invalid mood value"}, 400

    try:
        user_id = get_user_id_by_email()
        weather_data = get_tacker_weather_data()
        air_quality_data = get_air_quality()
        air_quality_index = air_quality_data['aqi']
        # Map moods to severity levels
        severity_map = {
            'Sad': 1,
            'Neutral': 3,
            'Happy': 5
        }
        
        # Save to symptom tracker table
        save_symptom_record(
            user_id=user_id,
            severity=severity_map[mood],
            mood=mood,
            temperature=weather_data['temperature'],
            humidity=weather_data['humidity'],
            wind_speed=weather_data['wind_speed'],
            weather_condition=weather_data['condition'],
            air_quality_index=round(air_quality_index),
            air_quality_status=get_aqi_category(air_quality_index)
        )

        flash(f"Successfully logged your mood: {mood}", "success")
        return {"success": True}, 200
    except Exception as e:
        flash("Error saving your mood", "error")
        return {"error": str(e)}, 500


# Define error handlers for various HTTP status codes
@app.errorhandler(404)
def page_not_found(e):
    flash('Page not found', 'error')
    return redirect("/")  

@app.errorhandler(500)
def internal_server_error(e):
    flash('Internal server error', 'error')
    return redirect("/")
@app.errorhandler(405)
def method_not_allowed(e):
    flash('Method not allowed', 'error')
    return redirect("/")
@app.errorhandler(403)
def forbidden(e):
    flash('Access denied', 'error')
    return redirect("/")
@app.errorhandler(401)
def unauthorized(e):
    flash('Unauthorized access', 'error')
    return redirect("/")
@app.errorhandler(400)
def bad_request(e):
    flash('Bad request', 'error')
    return redirect("/")
@app.errorhandler(413)
def request_entity_too_large(e):
    flash('Request entity too large', 'error')
    return redirect("/")
@app.errorhandler(Exception)
def handle_exception(e):
    flash('An unexpected error occurred. Please try again later.', 'error')
    return redirect("/")

if __name__ == "__main__":
    set_up_db()
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s: %(message)s')
    app.run(host="0.0.0.0", port=5000)
    # app.run(debug=True)