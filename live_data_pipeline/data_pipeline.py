import serial
import sys
import datetime
import time
import requests

# data_pipeline.py
#
# Usage:
#       python data_pipeline.py <COM_PORT> <BAUD>


URL = "http://192.168.1.125:8000/api/temperature_sensor/"

if len(sys.argv) < 3:
    print("\nUsage:\n\tpython data_pipeline.py <COM_PORT> <BAUD>\n")
    sys.exit(0)
    sys.exit(0)

try:
    ser = serial.Serial(sys.argv[1], sys.argv[2])
except:
    print(f"Port {sys.argv[1]} cannot be reached.")
    sys.exit(0)

cont = True

while cont:
    ser_bytes = ser.readline()
    decoded_bytes = float(ser_bytes[0:len(ser_bytes)-2].decode("utf-8"))
    print(decoded_bytes)
    request_time = time.time() 
    rounded_down_time = request_time - request_time % 60 
    print(rounded_down_time)
    try:
        req = requests.post(URL, data = {"sensor": 1,
                                "time": int(rounded_down_time),
                                "temperature": round(decoded_bytes, 1)})
        print(req.status_code)
    except:
        print("error")
    time.sleep(5)

