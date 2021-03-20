import serial
import sys
import datetime
import time
import requests

# data_pipeline.py
#
# Usage:
#       python data_pipeline.py <COM_PORT> <BAUD>


# Server URL
URL = "http://192.168.1.125:8000/api/temperature_sensor/"

# Check for argument length; Exit if fewer than 2 arguments given
if len(sys.argv) < 3:
    print("\nUsage:\n\tpython data_pipeline.py <COM_PORT> <BAUD>\n")
    sys.exit(0)

# Attempts to establish a serial connection with the port specified
try:
    ser = serial.Serial(sys.argv[1], sys.argv[2])
except:
    print(f"Port {sys.argv[1]} cannot be reached.")
    sys.exit(0)


while True:
    # Read serial data
    ser_bytes = ser.readline()
    decoded_bytes = float(ser_bytes[0:len(ser_bytes)-2].decode("utf-8"))

    # Set time of the reading to the current time
    request_time = time.time() 

    # Round down epoch to nearest minute
    rounded_down_time = request_time - request_time % 60 

    print(decoded_bytes)

    try:
        req = requests.post(URL, data = {"sensor": 1,
                                "time": int(rounded_down_time),
                                "temperature": round(decoded_bytes, 1)})
        print(req.status_code)
    except:
        print("error")
    time.sleep(5)

