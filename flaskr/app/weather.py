import requests
from flask import flash
import google.generativeai as genai
import os
from dotenv import load_dotenv
import json
import sqlite3

from auth import get_user_id_by_email

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


def get_ai_assesment_tips():
    """
    Generate AI-powered risk assessment tips based on user data and air quality.

    Returns:
        list: A list of dictionaries containing risk titles and detailed mitigation advice.
    """
    # Get assessment from database
    user_id = get_user_id_by_email()
    conn = sqlite3.connect('Health.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM risk_assessments WHERE user_id = ?", (user_id,)) 
    assessment_data = cursor.fetchone()
    conn.close()

    # Get weather data
    air_quality = get_air_quality()

    # Get AI response with simplified prompt
    prompt = (
        f"Conduct a professional risk assessment of a residential property, evaluating potential hazards related to weather, environmental factors, and health concerns. "
        f"Assess risks such as flooding, extreme temperatures, mold growth, and air quality. "
        f"Include considerations for allergies, such as pollen levels (hay fever risk), dust mites, pet dander, and potential indoor pollutants. "
        f"Provide a detailed analysis with mitigation strategies to improve safety and livability. "
        f"Assessment Data: {assessment_data} "
        f"Air Quality: {air_quality} "
        f"### Requirements: "
        f"1. Identify at least 5 specific hazards or risks. "
        f"2. Provide detailed mitigation strategies for each risk. "
        f"3. If necessary, recommend a professional assessment from a health advisory group (the same website this is hosted on). "
        f"4. YOU MUST FOCUS ON THE USERS HOUSE"
        f"4. Respond in **valid JSON format**. "
        f"Return a 1 JSON array of the  1 breakdown dont include multiple tips just 1 and tip is just placeholder its shoudl be more desctiobtion your not here to give tips your here to give a resk assesment in this exact format:\n"
        f"[{{\n"
        f"   \"title\": \"Risk Title\",\n"
        f"   \"tip\": \"Detailed mitigation advice\"\n"
        f"}}]\n\n"
        f"Each tip should identify a specific risk and provide detailed mitigation strategy."
    )

    try:
        response = model.generate_content(prompt)
        response_text = response.text.strip()

        # Remove markdown formatting if present
        if response_text.startswith("```"):
            response_text = response_text.split("```")[1]
            if response_text.startswith("json"):
                response_text = response_text[4:].trip()

        # Parse JSON and ensure it's a list
        response_data = json.loads(response_text)
        if isinstance(response_data, dict):
            response_data = [response_data]

        # Validate and clean each tip
        validated_tips = []
        for tip in response_data:
            if isinstance(tip, dict) and 'title' in tip and 'tip' in tip:
                validated_tips.append({
                    'title': str(tip['title']),
                    'tip': str(tip['tip'])
                })

        return validated_tips or [{
            'title': 'No risks identified',
            'tip': 'Unable to analyze data at this time.'
        }]
    
    except Exception as e:
        flash(f"Error generating AI tips: {str(e)}", "error")
        return [{
            'title': 'Error',
            'tip': 'Unable to generate assessment at this time.'
        }]


def get_aqi_category(aqi):
    """
    Categorize AQI value into quality groups.

    Args:
        aqi (int): The Air Quality Index value.

    Returns:
        str: The category of air quality.
    """
    aqi = int(aqi)
    if aqi <= 50: return 'Moderate'
    elif aqi <= 100: return 'good'
    elif aqi <= 150: return 'Bad'
    elif aqi <= 200: return 'Unhealthy'
    else: return 'Hazard'


def get_tacker_weather_data():
    """Fetch weather data from Open-Meteo API"""
    
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": 51.2362,  # Horsham coordinates
        "longitude": -0.3360,
        "hourly": [
            "temperature_2m",
            "relative_humidity_2m", 
            "wind_speed_10m",
            "weather_code"
        ],
        "forecast_days": 1
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()

        # Get current hour's data (first element)
        current_data = {
            'temperature': data['hourly']['temperature_2m'][0],
            'humidity': data['hourly']['relative_humidity_2m'][0],
            'wind_speed': data['hourly']['wind_speed_10m'][0],
            'condition': get_weather_condition(data['hourly']['weather_code'][0]),
        }
        
        return current_data

    except requests.RequestException as e:
        print(f"Error fetching weather data: {e}")
        return {}

def get_weather_condition(code: int) -> str:
    """Convert weather code to readable condition"""
    conditions = {
        0: "Clear sky",
        1: "Mainly clear",
        2: "Partly cloudy",
        3: "Overcast",
        45: "Foggy",
        48: "Rime fog",
        51: "Light drizzle",
        53: "Moderate drizzle",
        55: "Dense drizzle",
        61: "Light rain",
        63: "Moderate rain",
        65: "Heavy rain",
        71: "Light snow",
        73: "Moderate snow",
        75: "Heavy snow",
        77: "Snow grains",
        80: "Light rain showers",
        81: "Moderate rain showers",
        82: "Violent rain showers",
    }
    return conditions.get(code, "Unknown")

def get_air_quality():
    """
    Get air quality data for health tips.

    Returns:
        dict: A dictionary containing air quality data.
    """
    city_name = get_location_from_ip()
    coordinates = get_coordinates(city_name)

    lat, lon = coordinates

    url = "https://air-quality-api.open-meteo.com/v1/air-quality"
    params = {
        "latitude": lat,
        "longitude": lon,
        "hourly": ["ozone", "aerosol_optical_depth", "european_aqi", "european_aqi_pm2_5", "european_aqi_pm10"]
    }

    try:
        # Fetch air quality data
        response = requests.get(url, params=params)
        response.raise_for_status()  # Raise an exception for bad status codes
        
        data = response.json()  # Parse the JSON response
        hourly = data.get('hourly', {})
        
        # Get the arrays of values
        hourly_ozone = hourly.get('ozone', [])
        hourly_aerosol = hourly.get('aerosol_optical_depth', [])
        hourly_aqi = hourly.get('european_aqi', [])
        hourly_pm25 = hourly.get('european_aqi_pm2_5', [])
        hourly_pm10 = hourly.get('european_aqi_pm10', [])

        # Calculate averages safely
        def safe_average(values):
            """
            Calculate average of values, filtering out None values.
            
            Args:
                values (list): List of numbers that may contain None values
                
            Returns:
                float: Average of non-None values, or 0 if no valid values
            """
            # Filter out None values
            valid_values = [v for v in values if v is not None]
            return sum(valid_values) / len(valid_values) if valid_values else 0

        return {
            "ozone": safe_average(hourly_ozone),
            "aerosol": safe_average(hourly_aerosol),
            "aqi": safe_average(hourly_aqi),
            "pm2_5": safe_average(hourly_pm25), 
            "pm10": safe_average(hourly_pm10)
        }

    except requests.RequestException as e:
        flash(f"Error fetching air quality data: {str(e)}", "error")
        return None
    except ValueError as e:
        flash(f"Error parsing air quality data: {str(e)}", "error")
        return None


def get_air_ai_tips():
    """
    Generate air quality insights and recommendations based on user health conditions.

    Returns:
        dict: A dictionary containing AQI, summary, and recommendations.
    """
    response_template = {
        "AQI": "",
        "summary": "",
        "recommendations": ""
    }

    # Initialize default values
    conditions = None
    user_id = None
    air_quality = None
    city_name = "your area"

    try:
        # Get user information
        try:
            user_id = get_user_id_by_email()
        except Exception as e:
            print("User not signed in, proceeding anonymously", "info")

        # Get health conditions if user is logged in
        if user_id:
            conn = sqlite3.connect('Health.db')
            try:
                with conn:
                    cursor = conn.cursor()
                    cursor.execute("SELECT crd FROM users WHERE id = ?", (user_id,))
                    result = cursor.fetchone()
                    conditions = result[0] if result else None
            finally:
                conn.close()

        # Get environmental data
        air_quality = get_air_quality()
        city_name = get_location_from_ip() or "your area"

        prompt = f"""
        Generate a concise air quality summary and health recommendations for {city_name}.
        User health conditions: {conditions}
        Current air quality data: {air_quality}

        Requirements:
        1. Structure response as valid JSON
        2. Include AQI value, summary, and recommendations
        3. Keep recommendations practical and specific to the air quality data
        4. Mention any relevant considerations for the user's health conditions

        Example format:
        {{
            "AQI": "AQI_VALUE",
            "summary": "Brief air quality summary...",
            "recommendations": "Specific health recommendations..."
        }}
        """

        # Generate and validate response
        response = model.generate_content(prompt)
        response_text = response.text.strip()

        # Ensure the response is in the expected JSON format
        if response_text.startswith("```json"):
            response_text = response_text[7:-3].strip()

        response_data = json.loads(response_text)

        # Validate response structure
        if not all(key in response_data for key in response_template):
            raise ValueError("Invalid response structure from AI model")

        return response_data

    except json.JSONDecodeError as e:
        flash(f"JSON parsing failed: {str(e)}", "error")
        return {"error": "Failed to parse AI response"}
    except Exception as e:
        flash(f"Error generating tips: {str(e)}", "error")
        return {"error": "Unable to generate recommendations at this time"}


def get_weather_conditions():
    """
    Get weather conditions for health tips.

    Returns:
        dict: A dictionary containing current and average weather conditions.
    """
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
    """
    Generate AI-generated health tips using Generative AI model.

    Returns:
        str: AI-generated health tips in JSON format.
    """
    # Get Conditions From Database

    try:
        user_id = get_user_id_by_email()
    except Exception as e:
        flash(f"Not Signed In", "warning")
        conditions = "None"
    else:
        conn = sqlite3.connect('Health.db')
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
    """
    Get user's location based on IP address.

    Returns:
        str: The city name based on the user's IP address.
    """
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
    """
    Convert city name to latitude and longitude.

    Args:
        city_name (str): The name of the city.

    Returns:
        tuple: A tuple containing latitude and longitude.
    """
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
    """
    Fetch weather forecast for given coordinates.

    Args:
        lat (float): Latitude of the location.
        lon (float): Longitude of the location.

    Returns:
        dict: A dictionary containing weather forecast data.
    """
    try:
        weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&daily=temperature_2m_max,temperature_2m_min&timezone=auto"
        weather_response = requests.get(weather_url)
        weather_response.raise_for_status()
        return weather_response.json()
    except requests.RequestException:
        flash("Failed to fetch weather data.", "error")
        return None

def format_forecast_data(city_name, weather_data, tips):
    """
    Format the weather forecast data.

    Args:
        city_name (str): The name of the city.
        weather_data (dict): The raw weather data.
        tips (list): A list of health tips.

    Returns:
        dict: A dictionary containing formatted weather forecast data.
    """
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
    """
    Fetch raw weather data.

    Returns:
        tuple: A tuple containing the city name and raw weather data.
    """
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

    print (city_name, weather_data)
    return city_name, weather_data

def get_weather_data():
    """
    Main function to fetch and format weather data.

    Returns:
        dict: A dictionary containing formatted weather data and health tips.
    """
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

