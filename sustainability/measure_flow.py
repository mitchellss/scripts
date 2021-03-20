import sys 
import datetime
import pandas as pd

# measure_flow.py
#
# Author: Stephen Mitchell
# 
# Takes in USGS tab-separated 00060 Discharge data and computes the total
# volumentric flow.
#
# Example Usage:
#
# pip install -r requirements.txt
# python measure_flow.py flow.txt flow.csv

# Column number of datetime information
DATETIME_COL = 2

# Column number of flow information
FLOW_COL = 4

# Lines of data to be discarded
BAD_LINES = [*range(0,28),29]

# Opens original text file
with open(sys.argv[1], 'r') as text_file:
    lines = text_file.readlines()

# Writes new csv, replacing tabs with commas and removing erroneous lines
with open(sys.argv[2], "w") as csv_file:
    for line_num in range(0,len(lines)):
        if line_num not in BAD_LINES: 
            csv_file.write(lines[line_num].replace("\t", ","))

# Reads csv into pandas
file_data = pd.read_csv(sys.argv[2])

# Starts the total flow at zero
total_flow = 0

# Goes through each entry and does a Riemann sum using the last entry. Adds to total_flow
for line in range(1, len(file_data[file_data.columns[DATETIME_COL]])): 
    previous_measurement_datetime = datetime.datetime.strptime(file_data[file_data.columns[DATETIME_COL]][line-1], '%Y-%m-%d %H:%M')
    current_measurement_datetime = datetime.datetime.strptime(file_data[file_data.columns[DATETIME_COL]][line], '%Y-%m-%d %H:%M')
    total_flow += file_data[file_data.columns[FLOW_COL]][line] * (current_measurement_datetime.timestamp() - previous_measurement_datetime.timestamp())

# Prints results of calculation
print(f"{total_flow} cubic feet")