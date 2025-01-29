from flask import Flask, render_template, request, flash, redirect

from db import set_up_db,  add_user
from auth import sign_in, logout
from validation import is_not_empty, is_valid_email, is_within_length, is_secure_password



app = Flask(__name__, static_folder='../static')


app.secret_key = 'secret_key' 

@app.route("/")
def index():
    return render_template('index.html')

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



def get_weather(city):
    try:
        url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={APIkey}&units=metric"
        response = requests.get(url)
        data = response.json()
       
        if response.status_code == 200:
            return {
                'temperature': round(data['main']['temp']),
                'description': data['weather'][0]['description'],
                'icon': data['weather'][0]['icon']
            }
        return None
    except Exception as e:
        flash(f"Weather API error: {e}")
        return None



@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        return sign_in(email, password)

    return render_template("login.html")

if __name__ == "__main__":
    set_up_db()
    app.run(debug=True)