from flask import request, flash, Flask, jsonify
import requests

app = Flask(__name__)
app.secret_key ="🤫"

def get_location():
    ip = request.remote_addr
    print(f"ip === {ip}")
    try:
        response = requests.get(f"http://ip-api.com/json/{ip}")
        data = response.json()
        if data['status'] == 'fail':
            return None
        return {"latitude": data["lat"], "longitude": data["lon"], "city": data["city"], "country": data["country"]}
    except Exception as e:
        flash("An error occurred while trying to get your location", "error")
        return None

def get_weather():
    location = get_location()
    if not location:
        return jsonify({"error": "Could not determine location"})

    lat = location["latitude"]
    long = location["longitude"]

    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={long}&daily=temperature_2m_max,temperature_2m_min"
    try:
        response = requests.get(url)
        response.raise_for_status()
        weather_data = response.json()
        
        forecast = [
            {"day": "Today", "temp": f"{weather_data['daily']['temperature_2m_max'][0]}°"},
            {"day": "Tomorrow", "temp": f"{weather_data['daily']['temperature_2m_max'][1]}°"},
            {"day": "Day 3", "temp": f"{weather_data['daily']['temperature_2m_max'][2]}°"},
            {"day": "Day 4", "temp": f"{weather_data['daily']['temperature_2m_max'][3]}°"},
            {"day": "Day 5", "temp": f"{weather_data['daily']['temperature_2m_max'][4]}°"}
        ]
        
        return jsonify({
            "location": f"{location['city']}, {location['country']}",
            "forecast": forecast
        })
    except Exception as e:
        return jsonify({"error": str(e)})

@app.route('/weather')
def weather():
    return get_weather()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)