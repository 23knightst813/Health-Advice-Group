import requests
from flask import flash
import google.generativeai as genai
import os
from dotenv import load_dotenv
import json

from auth import get_user_id_by_email
from db import get_db_connection


# Load environment variables
try:
    load_dotenv()
    API_KEY = os.getenv("GEMINI_API_KEY")
except Exception as e:
    flash(f"Error loading environment variables: {str(e)}", "error")

# Set up generative AI model
try:    
    if not API_KEY:
        flash("GEMINI_API_KEY not found in environment variables", "error")
        raise ValueError("API key not found")

    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel("gemini-1.5-flash")
    
except ValueError as e:
    flash(f"Error loading Generative AI API: {str(e)}", "error")

def get_weather_conditions():
    """Get weather conditions for health tips."""
    city_name = get_location_from_ip()
    if not city_name:
        return None

    coordinates = get_coordinates(city_name)
    if not coordinates:
        return None
    
    lat, lon = coordinates
    
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat,
        "longitude": lon,
        "hourly": ["weather_code", "vapour_pressure_deficit", "wind_speed_10m", "soil_moisture_0_to_1cm"]
    }
    response = requests.get(url, params=params)

    # Store the response data
    weather_data = response.json()

    # Extract hourly data 
    hourly_weather_code = weather_data['hourly']['weather_code'][0]
    hourly_vapour_pressure_deficit = weather_data['hourly']['vapour_pressure_deficit'][0]
    hourly_wind_speed_10m = weather_data['hourly']['wind_speed_10m'][0]
    hourly_soil_moisture_0_to_1cm = weather_data['hourly']['soil_moisture_0_to_1cm'][0]

    # Calculate averages
    avg_weather_code = sum(weather_data['hourly']['weather_code']) / len(weather_data['hourly']['weather_code'])
    avg_vapour_pressure = sum(weather_data['hourly']['vapour_pressure_deficit']) / len(weather_data['hourly']['vapour_pressure_deficit'])
    avg_wind_speed = sum(weather_data['hourly']['wind_speed_10m']) / len(weather_data['hourly']['wind_speed_10m'])
    avg_soil_moisture = sum(weather_data['hourly']['soil_moisture_0_to_1cm']) / len(weather_data['hourly']['soil_moisture_0_to_1cm'])

    return {
        "current": {
            "weather_code": hourly_weather_code,
            "vapour_pressure": hourly_vapour_pressure_deficit,
            "wind_speed": hourly_wind_speed_10m,
            "soil_moisture": hourly_soil_moisture_0_to_1cm
        },
        "averages": {
            "weather_code": round(avg_weather_code, 2),
            "vapour_pressure": round(avg_vapour_pressure, 2),
            "wind_speed": round(avg_wind_speed, 2), 
            "soil_moisture": round(avg_soil_moisture, 3)
        }
    }

def get_ai_tips():
    """Generate AI-generated health tips using Generative AI model."""
    
    #Get Conditions From Database

    try:
        user_id = get_user_id_by_email()
    except Exception as e:
        flash(f"Not Signed In", "error")
        conditions = "None"
    else:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT crd FROM users WHERE id = ?", (user_id,))
        conditions = cursor.fetchone()
        conn.close()

    city_name, weather_data = raw_weather()

    current_weather_conditions = get_weather_conditions()

    prompt = f"""
    Generate one specific health tip for someone with {conditions} based on today's weather conditions in and Environmental Factors {city_name}.
    Weather: {weather_data}
    Environmental Factors: {current_weather_conditions}

    Requirements:
    2. Consider temperature effects
    3. Make it practical and actionable
    4. Keep it very detialed
    5. Provide at 3 of the most relevant tips
    6. USE  Environmental Factors
    7. Mention the users condition if they have any 
    8. Return ONLY valid JSON without any additional formatting or text
    9. Only have 15 lines of advice total maximum

    Format your response EXACTLY like this example:
    {{"title": "Weather Alert e.g High wind", "tip": "specific scientific health advice"}}

    Your response must be valid JSON and nothing else.
    """

    try:
        tips = model.generate_content(prompt)
        print(tips.text.strip())
        return tips.text.strip()

    except Exception as e:
        flash(f"Error generating AI tips: {str(e)}", "error")
        return None

def get_location_from_ip():
    """Get user's location based on IP address."""
    try:
        ip_response = requests.get("https://ipinfo.io/json")
        ip_response.raise_for_status()
        ip_data = ip_response.json()

        if 'city' not in ip_data:
            flash("City not found in IP data.", "error")
            return None
        
        return ip_data['city']
    except requests.RequestException:
        flash("Failed to fetch location from IP.", "error")
        return None

def get_coordinates(city_name):
    """Convert city name to latitude and longitude."""
    try:
        geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city_name}"
        geo_response = requests.get(geo_url)
        geo_response.raise_for_status()
        geo_data = geo_response.json()

        if "results" not in geo_data:
            flash("City not found in geocoding API.", "error")
            return None

        city = geo_data['results'][0]
        return city['latitude'], city['longitude']
    except requests.RequestException:
        flash("Failed to fetch coordinates.", "error")
        return None

def fetch_weather_forecast(lat, lon):
    """Fetch weather forecast for given coordinates."""
    try:
        weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&daily=temperature_2m_max,temperature_2m_min&timezone=auto"
        weather_response = requests.get(weather_url)
        weather_response.raise_for_status()
        return weather_response.json()
    except requests.RequestException:
        flash("Failed to fetch weather data.", "error")
        return None

def format_forecast_data(city_name, weather_data, tips):
    """Format the weather forecast data."""
    return {
        "location": city_name.capitalize(),
        "forecast": [
            {"day": "Today", "temp": f"{weather_data['daily']['temperature_2m_max'][0]}°C"},
            {"day": "Tomorrow", "temp": f"{weather_data['daily']['temperature_2m_max'][1]}°C"},
            {"day": "Day 3", "temp": f"{weather_data['daily']['temperature_2m_max'][2]}°C"},
            {"day": "Day 4", "temp": f"{weather_data['daily']['temperature_2m_max'][3]}°C"},
            {"day": "Day 5", "temp": f"{weather_data['daily']['temperature_2m_max'][4]}°C"}
        ],
        "health_tips": tips  
    }

def raw_weather():
    """Fetch raw weather data"""
    city_name = get_location_from_ip()
    if not city_name:
        return None

    coordinates = get_coordinates(city_name)
    if not coordinates:
        return None
    
    lat, lon = coordinates
    weather_data = fetch_weather_forecast(lat, lon)
    if not weather_data:
        return None

    return city_name, weather_data

def get_weather_data():
    """Main function to fetch and format weather data."""
    try:
        # Get weather data
        result = raw_weather()
        if not result:
            return None
            
        city_name, weather_data = result
        
        # Get AI generated tips
        tips_text = get_ai_tips()
        if not tips_text:
            return None

        # Clean the response and parse JSON properly
        try:
            # Remove markdown backticks if present
            clean_tips = tips_text.strip().replace('```json', '').replace('```', '')
            
            # Parse the JSON array of tips
            tips = json.loads(clean_tips)
            
            # Ensure tips is a list
            if isinstance(tips, dict):
                tips = [tips]
            
        except json.JSONDecodeError as e:
            flash(f"Error parsing AI tips: {str(e)}", "error")
            print(f"Raw AI response: {tips_text}")
            return None
        
        # Format forecast data
        formatted_data = format_forecast_data(city_name, weather_data, tips)
        return formatted_data
        
    except Exception as e:
        flash(f"Error in get_weather_data: {str(e)}", "error")
        return None
