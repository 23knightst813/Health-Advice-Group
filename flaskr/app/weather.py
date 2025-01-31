import datetime
import requests
from flask import flash
import google.generativeai as genai
import os
from dotenv import load_dotenv

#Load env varibles

load_dotenv()

#Load the API key from the environment variable
API_KEY = os.getenv("GEMINI_API_KEY")

genai.configure(api_key="GEMINI_API_KEYY")
model = genai.GenerativeModel("gemini-1.5-flash")
response = model.generate_content("Explain how AI works")
print(response.text)



def get_weather_data():
    """Fetch user's location and retrieve weather forecast based on latitude and longitude."""
    try:
        # Step 1: Get user's approximate location based on IP
        ip_response = requests.get("https://ipinfo.io/json")
        ip_response.raise_for_status()
        ip_data = ip_response.json()

        if 'city' not in ip_data:
            flash("City not found in IP data.", "error")
            return None

        city_name = ip_data['city']

        # Step 2: Convert city name to latitude & longitude
        geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city_name}"
        geo_response = requests.get(geo_url)
        geo_response.raise_for_status()
        geo_data = geo_response.json()

        if "results" not in geo_data:
            flash("City not found in geocoding API.", "error")
            return None

        city = geo_data['results'][0]
        lat, lon = city['latitude'], city['longitude']

        # Step 3: Fetch weather forecast using lat & lon
        weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&daily=temperature_2m_max,temperature_2m_min&timezone=auto"
        weather_response = requests.get(weather_url)
        weather_response.raise_for_status()
        weather_data = weather_response.json()

        # Step 4: Format the forecast data
        forecast = {
            "location": city_name.capitalize(),
            "current_time": datetime.datetime.now().strftime("%H:%M"),
            "forecast": [
                {"day": "Today", "temp": f"{weather_data['daily']['temperature_2m_max'][0]}°C"},
                {"day": "Tomorrow", "temp": f"{weather_data['daily']['temperature_2m_max'][1]}°C"},
                {"day": "Day 3", "temp": f"{weather_data['daily']['temperature_2m_max'][2]}°C"},
                {"day": "Day 4", "temp": f"{weather_data['daily']['temperature_2m_max'][3]}°C"},
                {"day": "Day 5", "temp": f"{weather_data['daily']['temperature_2m_max'][4]}°C"}
            ],
            "health_tips": [
                {"title": "High AQI (Air Quality Index):", "tip": "Avoid outdoor activities if you have respiratory conditions like asthma."},
                {"title": "High Pollen Count:", "tip": "Keep windows closed and wash your hands and face after being outside."}
            ]
        }
        print(city_name)
        return forecast

    except requests.RequestException as e:
        flash(f"Error retrieving data: {str(e)}", "error")
        return None

