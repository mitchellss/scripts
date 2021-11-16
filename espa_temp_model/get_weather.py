import requests
import os
import yaml
from datetime import datetime, time, timedelta
import matplotlib.pyplot as plt
import sys
import argparse

####################################################################
#
# EXAMPLE USAGE:
#       python get_weather.py --time 20:00 --temp 40
#       
#       This will return the predicted temperature 20 hours
#       in the future (in Harrisonburg) based on the a 
#       current measured temperature of 40 degrees Fahrenheit
#
####################################################################


parser = argparse.ArgumentParser(description="Predict temperature based on future forecast data and current difference")
parser.add_argument("--file", nargs="?", help="The future temperature file to use (.yaml format). Ommit to use live data.")
parser.add_argument("--time", type=str, nargs="?", default="02:00", help="How many hours and minutes into the future to guess the temperature (HH:MM) up to 48:00")
parser.add_argument("--temp", type=float, nargs="?", default=20.0, help="The current measured temperature in fahrenheit")
args = parser.parse_args()

def k_to_f(temp):
    return (temp - 273.15) * 1.8 + 32

measured_temp = args.temp

# Coords for Harrisonburg
lat_lon = (38.443731, -78.866172)

try:
    key = os.environ['OPENWEATHER_KEY']
except:
    print("Cannot find environment variable key, using string (might not be correct)")
    key = "REPLACE THIS WITH THE KEY"

url = f"https://api.openweathermap.org/data/2.5/onecall?lat={lat_lon[0]}&lon={lat_lon[1]}&exclude=daily,minutely&appid={key}"

if args.file is not None:
    try:
        print("Using temperature data from file...")
        with open(args.file, "r") as file:
            data = yaml.safe_load(file)
    except:
        print("File cannot be opened")
        sys.exit(1)
else:
    print("Getting live data...")
    data = requests.get(url).json()


curr_api_temp = data['current']['temp']
temp_diff =  measured_temp - k_to_f(curr_api_temp)
hourly_forcast = data['hourly']

# Create list of hourly temps and our predicted minutely temps
forcast_temp = []
our_predicted_temp = []
for i in range(0,len(hourly_forcast)):
    fahrenheit_temp = k_to_f(hourly_forcast[i]['temp'])
    forcast_temp.append(fahrenheit_temp)

    # Interpolate data up to the minute based on forcasted data
    if i != len(hourly_forcast)-1:
        fahrenheit_temp_2 = k_to_f(hourly_forcast[i+1]['temp'])
        for j in range(0,60):
            our_predicted_temp.append(fahrenheit_temp + ((j/60)*(fahrenheit_temp_2-fahrenheit_temp)) + temp_diff)
    
# Convert time argument into an index and find the temp at that index
time_index = int(args.time.split(":")[0])*60 + int(args.time.split(":")[1])
time_val = our_predicted_temp[time_index]
print(f"{round(time_val,2)} F")

plt.plot(range(0,len(our_predicted_temp)+1,60), forcast_temp)
plt.plot(our_predicted_temp)
plt.vlines(time_index, min(our_predicted_temp), max(our_predicted_temp), colors="orange")
plt.show()
