from flask import Flask, request, jsonify
import requests
from datetime import datetime

app = Flask(__name__)

OPENWEATHER_API_KEY = '674fd6a87afe1f1aecc15f659fe776ad'

@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json()
    intent = req.get('queryResult').get('intent').get('displayName')
    city = req.get('queryResult').get('parameters').get('geo-city')

    if intent == 'CurrentWeatherIntent':
        if city:
            weather = get_current_weather(city)
            if weather:
                response = {
                    "fulfillmentText": weather
                }
            else:
                response = {
                    "fulfillmentText": "I'm sorry, I couldn't find the weather for that city."
                }
        else:
            response = {
                "fulfillmentText": "Please provide a city to get the weather information."
            }
    elif intent == 'WeatherForecastIntent':
        if city:
            forecast = get_weather_forecast(city)
            if forecast:
                response = {
                    "fulfillmentText": forecast
                }
            else:
                response = {
                    "fulfillmentText": "I'm sorry, I couldn't find the weather forecast for that city."
                }
        else:
            response = {
                "fulfillmentText": "Please provide a city to get the weather forecast."
            }

    return jsonify(response)

def get_current_weather(city):
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid=OPENWEATHER_API_KEY &units=metric'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        weather = f"Current temperature in {city} is {data['main']['temp']}°C with {data['weather'][0]['description']}."
        return weather
    else:
        return None

def get_weather_forecast(city):
    url = f'http://api.openweathermap.org/data/2.5/forecast/daily?q={city}&cnt=8&appid=OPENWEATHER_API_KEY &units=metric'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        forecast = f"3-day weather forecast for {city}:\n"
        for day in data['list']:
            date = datetime.utcfromtimestamp(day['dt']).strftime('%Y-%m-%d')
            temp = day['temp']['day']
            description = day['weather'][0]['description']
            forecast += f"{date}: {temp}°C, {description}\n"
        return forecast
    else:
        return None

if __name__ == '__main__':
    app.run(port=5000)
