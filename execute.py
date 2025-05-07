import time
import requests
from datetime import datetime
import json

# API Keys
TOMORROW_API_KEY = "TOMORROW_API_KEY"
GEMINI_API_KEY = "GEMINI_API_KEY"

def get_weather_data(location):
    """Fetch weather and soil data"""
    url = f"https://api.tomorrow.io/v4/weather/realtime?location={location}&apikey={TOMORROW_API_KEY}"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()

        values = data.get('data', {}).get('values', {})
        temperature = values.get('temperature', None)  # Temperature (°C)
        humidity = values.get('humidity', None)        # Humidity (%)
        rainfall = values.get('precipitationIntensity', 0)  # Rainfall (mm/hr)

        return temperature, humidity, rainfall

    except Exception as e:
        print(f"Failed to fetch weather data: {e}")
        return None, None, None

def get_ai_crop_recommendation(location, temperature, humidity):
    """Fetch crop recommendations from Gemini API based on location and weather"""
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GEMINI_API_KEY}"
    headers = {
        'Content-Type': 'application/json'
    }

    # Generate a dynamic prompt for crop recommendations based on weather
    prompt = (
        f"Based on the weather in {location}, with a temperature of {temperature}°C and humidity of {humidity}%, "
        "recommend crops that are suitable for growing in this climate."
    )

    data = {
        "contents": [{
            "parts": [{"text": prompt}]
        }]
    }

    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()  # Raise an error for bad status codes
        response_data = response.json()

        # Extracting the AI-generated crop recommendation from the response
        recommended_text = response_data['contents'][0]['parts'][0]['text']
        return recommended_text

    except requests.exceptions.RequestException as e:
        print(f"Error fetching AI crop recommendations: {e}")
        return "Unable to fetch crop recommendations from AI."

def main():
    try:
        while True:
            # Get location input from user
            location = input("\nEnter location (e.g., Seoul, New York): ")

            # Fetch weather data (temperature, humidity)
            print("\nFetching weather data...")
            temperature, humidity, rainfall = get_weather_data(location)

            if temperature is not None and humidity is not None:
                print(f"\nWeather data for {location}:")
                print(f"Temperature: {temperature}°C")
                print(f"Humidity: {humidity}%")
                print(f"Rainfall: {rainfall} mm/hr")

                # AI-generated crop recommendations
                recommendation = get_ai_crop_recommendation(location, temperature, humidity)
                print("\nAI Crop Recommendations:")
                print(recommendation)

            else:
                print("Could not fetch valid weather data.")

            print("\n--- Refreshing in 30 seconds ---")
            time.sleep(30)
            
    except KeyboardInterrupt:
        print("\nStopping monitoring.")

if __name__ == "__main__":
    main()
