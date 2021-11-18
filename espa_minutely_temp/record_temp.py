import requests
import time
import json
import os

key = ""

# Coords for Harrisonburg
lat_lon = (38.491487, -78.815965)

forecast_url = f"https://api.openweathermap.org/data/2.5/onecall?lat={lat_lon[0]}&lon={lat_lon[1]}&exclude=daily,minutely&appid={key}"
current_temp_url = f"https://api.openweathermap.org/data/2.5/weather?q=harrisonburg&appid={key}"

count = 0

def k_to_f(temp):
    return (temp - 273.15) * 1.8 + 32

while True:
    data = requests.get(current_temp_url).json()

    temperature_file = open("temperature_file.csv", "a")
    temperature_file.write(f"{time.time()},{round(k_to_f(data['main']['temp']), 3)}\n")

    if count % 60 == 0:
        data2 = requests.get(forecast_url).json()
        f = open(f"{int(time.time())}.json", "w+")
        json.dump(data2,f)
        f.close()

    count += 1
    temperature_file.close()

    time.sleep(60)