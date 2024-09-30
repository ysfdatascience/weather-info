import requests
import sys
from pprint import pp
sys.stdout.reconfigure(encoding = "utf-8")
from datetime import datetime
import json
from send_message import send_email

"""Retrieving the coordinates of the location for which the weather will be checked using the GeoCoding API."""
##############################################################################################################

with open("config.json") as file:
    data = json.load(file)
    api = data["api_key"]
    password = data["app_password_gmail"]


api_key = api
geocoding_enpoint = "http://api.openweathermap.org/geo/1.0/direct?"

weather_enpoint = ""
geo_params = {
    "q": "Ümraniye",
    "appid": api_key,
    "limit": 1
}


geo_response = requests.get(url=geocoding_enpoint, params=geo_params)
geo_response.raise_for_status()
geo_loc_data =  geo_response.json()

my_loc = geo_loc_data[0]["local_names"]["tr"]
my_lat = geo_loc_data[0]["lat"]
my_lon = geo_loc_data[0]["lon"]

print(f"{my_loc} kordinatları lat: {my_lat}, lon: {my_lon}")

"""Retrieving weather data via API and converting it to info_text."""
##############################################################################################################

openweather_api_endpoint = "https://api.openweathermap.org/data/2.5/weather?"

weather_params = {
    "lat": my_lat,
    "lon": my_lon,
    "appid": api_key,
    "units": "metric",
    "lang": "tr"
}

weather_response = requests.get(url=openweather_api_endpoint, params=weather_params)
weather_response.raise_for_status()
weather_data = weather_response.json()

# Converting timestamps to date-time format.
data_time = datetime.fromtimestamp(weather_data["dt"]).strftime("%d-%m-%Y %H:%M:%S")
sunrise = datetime.fromtimestamp(weather_data["sys"]["sunrise"]).strftime("%H:%M:%S")
sunset = datetime.fromtimestamp(weather_data["sys"]["sunset"]).strftime("%H:%M:%S")

# creating info_text

info_text = f"""{data_time} itibariyle {weather_data["name"]} bölgesindeki hava durumu: 
- Sıcaklık: {weather_data["main"]["temp"]}°C
- Minimum Sıcaklık : {weather_data["main"]["temp_min"]}°C (Hissedilen Sıcaklık: {weather_data["main"]["feels_like"]}°C)
- Hava Durumu: {weather_data["weather"][0]["description"].capitalize()}
- Nem %{weather_data["main"]["humidity"]}
- Basınç: {weather_data['main']['pressure']} hPa
- Görüş Mesafesi: {weather_data['visibility']} metre
- Rüzgar: {weather_data['wind']['speed']} m/s, Yön: {weather_data['wind']['deg']}°, Rüzgar Hızı (Gust): {weather_data['wind']['gust']} m/s
- Bulut Oranı: %{weather_data['clouds']['all']}
- Güneşin Doğuşu: {sunrise} UTC, Güneşin Batışı: {sunset} UTC """

##############################################################################################################
"""Sending email with smtplib"""

send_email("ysfylmz_1218@hotmail.com", password=password, content=info_text)
