import sys 
import datetime
import pandas as pd

DATETIME_COL = 2
FLOW_COL = 4

with open(sys.argv[1], 'r') as text_file:
    lines = text_file.readlines()
with open(sys.argv[2], "w") as csv_file:
    for line_num in range(0,len(lines)):
        if line_num > 27 and line_num != 29:
            csv_file.write(lines[line_num].replace("\t", ","))

file_data = pd.read_csv(sys.argv[2])
total_flow = 0

date = file_data['datetime'][0]

date_time_obj = datetime.datetime.strptime(date, '%Y-%m-%d %H:%M')


for i in range(1,len(file_data[file_data.columns[DATETIME_COL]])): 
    previous_measurement_datetime = datetime.datetime.strptime(file_data[file_data.columns[DATETIME_COL]][i-1], '%Y-%m-%d %H:%M')
    current_measurement_datetime = datetime.datetime.strptime(file_data[file_data.columns[DATETIME_COL]][i], '%Y-%m-%d %H:%M')
    #if previous_measurement_datetime >= datetime.datetime(2020,5,17) and previous_measurement_datetime <= datetime.datetime(2020,5,24):
    total_flow += file_data[file_data.columns[FLOW_COL]][i] * (current_measurement_datetime.timestamp() - previous_measurement_datetime.timestamp())

print(total_flow)