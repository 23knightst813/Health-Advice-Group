import requests



response = requests.get("https://ipinfo.io/json")
data = response.json()

city_name = data['city']

print(city_name)

geocoding_url = f'https://geocoding-api.open-meteo.com/v1/search?name={city_name}'
response = requests.get(geocoding_url)
data = response.json()

if 'results' in data:
    city = data['results'][0]
    lat = city['latitude']
    long = city['longitude']
    print(f"Coordinates for {city_name}: {lat}, {long}")
else:
    print("City not found.")

url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={long}&daily=temperature_2m_max,temperature_2m_min"

response = requests.get(url)
response.raise_for_status()
weather_data = response.json()

print(weather_data)

forecast = [
    {"day": "Today", "temp": f"{weather_data['daily']['temperature_2m_max'][0]}°"},
    {"day": "Tomorrow", "temp": f"{weather_data['daily']['temperature_2m_max'][1]}°"},
    {"day": "Day 3", "temp": f"{weather_data['daily']['temperature_2m_max'][2]}°"},
    {"day": "Day 4", "temp": f"{weather_data['daily']['temperature_2m_max'][3]}°"},
    {"day": "Day 5", "temp": f"{weather_data['daily']['temperature_2m_max'][4]}°"}
]

print(forecast)