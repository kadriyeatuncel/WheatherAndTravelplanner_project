import os
import requests
from flask import Flask, render_template, request

app = Flask(__name__)

# Weather codes mapping for Open-Meteo
WEATHER_CODES = {
    0: "Clear sky", 1: "Mainly clear", 2: "Partly cloudy", 3: "Overcast",
    45: "Fog", 48: "Rime fog", 51: "Light drizzle", 61: "Slight rain",
    63: "Moderate rain", 65: "Heavy rain", 71: "Slight snow", 95: "Thunderstorm"
}

def get_live_weather():
    """Fetches real-time Munich weather, humidity, and wind."""
    # Munich Coordinates
    lat, lon = 48.1351, 11.5820 
    weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m,relative_humidity_2m,weather_code,wind_speed_10m&timezone=Europe%2FBerlin"
    aqi_url = f"https://air-quality-api.open-meteo.com/v1/air-quality?latitude={lat}&longitude={lon}&current=european_aqi"
    
    try:
        weather_response = requests.get(weather_url)
        aqi_response = requests.get(aqi_url)
        weather_data = weather_response.json()["current"]
        aqi_data = aqi_response.json()["current"]
        return {
            "temp": round(weather_data["temperature_2m"]),
            "humidity": weather_data["relative_humidity_2m"],
            "wind": round(weather_data["wind_speed_10m"]),
            "code": weather_data["weather_code"],
            "desc": WEATHER_CODES.get(weather_data["weather_code"], "Cloudy"),
            "aqi_status": aqi_data["european_aqi"]
        }
    except Exception as e:
        print(f"Weather Error: {e}")
        return {"temp": 15, "humidity": 50, "wind": 10, "desc": "Connection Error"}

def generate_todos(weather, user_info):
    tasks = ["Start your day with a fresh Bavarian Brezel! 🥨"]
    
    # Weather & Wind& Air Quality Logic
    if weather['wind'] > 25:
        tasks.append("Warning: High winds! Avoid high viewpoints and park trees 🌬️")
    
    if weather['code'] >= 51: # Rain/Snow codes
        tasks.append("It's raining/snowing: Explore the world-class 'Deutsches Museum' 🏛️")
    elif weather['temp'] > 22:
        tasks.append("Warm weather: Visit the English Garden and watch the Eisbach surfers 🏄")
    else:
        tasks.append("Walk through Marienplatz and watch the Glockenspiel performance 🏰")

    if weather['aqi_status'] <= 40:
             tasks.append("Good Air Quality:Perfect for a walk in Englischer Garten! 🌿")
    
    else:
            tasks.append("Bad Air Quality: Limit outdoor activities 🚫")

    # Disability Logic
    if user_info.get('has_disability') == 'yes':
        tasks.append("Accessibility Tip: Use 'MVV Barrier-free' for real-time elevator status ♿")
        tasks.append("Visit the Pinakothek museums – they offer excellent wheelchair access 🖼️")
    else:
        tasks.append("Climb the 'Alter Peter' church tower for a panoramic city view 🗼")

    # Dog Friendly Logic
    if user_info.get('has_dog') == 'yes':
        tasks.append("Dog Friendly: Take a long walk in the Olympiapark – it's huge and dog-friendly 🐕")
        tasks.append("Note: Most Munich Beer Gardens welcome dogs with open arms! 🐾")

    # Car Logic
    if user_info.get('has_car') == 'yes':
        tasks.append("Car Tip: Use 'Park & Ride' lots to save money and avoid city traffic 🚗")
        
    #  Child Logic
    if user_info.get('has_child') == 'yes':
        tasks.append("With Kids: Visit the Toy Museum or the Hellabrunn Zoo 🦒")


    return tasks

@app.route('/')
def home():
    # Fixed: Now specifically calls your wireframe file
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    user_data = request.form.to_dict()
    weather = get_live_weather()
    todos = generate_todos(weather, user_data)
    return render_template('result.html', weather=weather, tasks=todos)
@app.route('/planner-form')

def planner_form():
    # Planner form route to display the form for user input
    return render_template('planner.html')


if __name__ == '__main__':
    app.run(debug=True, port=5000)


    