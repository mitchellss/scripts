import requests
import time
import json

key = ""

# Coords for Harrisonburg
lat_lon = (38.491487, -78.815965)

url = f"https://api.openweathermap.org/data/2.5/onecall?lat={lat_lon[0]}&lon={lat_lon[1]}&exclude=daily,minutely&appid={key}"
count = 0

def k_to_f(temp):
    return (temp - 273.15) * 1.8 + 32

while True:
    data = requests.get(url).json()

    temperature_file = open("temperature_file.csv", "a")
    temperature_file.write(f"{time.time()},{round(k_to_f(data['current']['temp']), 3)}\n")

    if count % 60 == 0:
        f = open(f"{int(time.time())}.json", "w+")
        json.dump(data,f)
        f.close()

    count += 1
    temperature_file.close()

    time.sleep(60)