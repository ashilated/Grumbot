from dotenv import load_dotenv
import requests
import os

load_dotenv()
key = os.getenv("OPENWEATHERMAP_API_KEY")

ipaddress = requests.get("https://api.ipify.org").content.decode("utf8")
grumbot_location = requests.get(f"https://geolocation-db.com/json/{ipaddress}&position=true").json()


def get_weather_data(weather):
    data = requests.get(weather)
    if data.status_code != 200:
        return -1

    return data.json()


def get_current_weather(location = None):
    if location is None:
        weather = f"https://api.openweathermap.org/data/2.5/weather?lat={grumbot_location['latitude']}&lon={grumbot_location['longitude']}&appid={key}&units=metric"
    else:
        weather = f"https://api.openweathermap.org/data/2.5/weather?q={location}&appid={key}&units=metric"

    data = get_weather_data(weather)

    temp = data['main']['temp']
    weather: str = data['weather'][0]['description']
    return {"temp": temp, "weather": weather}

def get_forecast(date, location = None):
    if location is None:
        weather = f"https://api.openweathermap.org/data/2.5/forecast?lat={grumbot_location['latitude']}lon={grumbot_location['longitude']}&cnt={date}&appid={key}&units=metric"
    else:
        weather = f"https://api.openweathermap.org/data/2.5/forecast?q={location}&cnt={date}&appid={key}&units=metric"

    data = get_weather_data(weather)

    temp = data['list'][-1]['main']['day']
    weather = data['list'][-1]['weather'][0]['description']
    return {"temp": temp, "weather": weather}


