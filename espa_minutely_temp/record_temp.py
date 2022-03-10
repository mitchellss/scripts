import requests
import time
import json
import os

key = "274c740b3b6b97ea519d485849454b59"

# Coords for Harrisonburg
lat_lon = (38.387328, -79.009110)

forecast_url = f"https://api.openweathermap.org/data/2.5/onecall?lat={lat_lon[0]}&lon={lat_lon[1]}&exclude=daily,minutely&appid={key}"
current_temp_url = f"https://api.openweathermap.org/data/2.5/weather?q=harrisonburg&appid={key}"

count = 0

def k_to_f(temp):
    return (temp - 273.15) * 1.8 + 32

while True:
    temperature_file = open("temperature_file.csv", "a")
    try:
        data = requests.get(current_temp_url).json()
        temperature_file.write(f"{time.time()},{round(k_to_f(data['main']['temp']), 3)}\n")
    except:
        print("error occured while getting current temp")

    temperature_file.close()

    if count % 60 == 0:
        f = open(f"{int(time.time())}.json", "w+")
        try:    
            data2 = requests.get(forecast_url).json()
            json.dump(data2,f)
        except:
            print("error occured while getting forecast")

        f.close()

    count += 1

    time.sleep(60)
