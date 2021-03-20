point_1 = {'lat': 37.932040344126456, 'lon': -78.49839270114899}
point_2 = {'lat': 37.932774442119374, 'lon': -78.49784016609192}
point_3 = {'lat': 37.93211306669711, 'lon': -78.49632706493139}
          
slope_1_2 = abs(point_2['lat'] - point_1['lat']) / (point_2['lon'] - point_1['lon'])
slope_2_3 = abs(point_3['lat'] - point_2['lat']) / (point_3['lon'] - point_2['lon'])

lat_1_2 = (point_2['lat'] - point_1['lat'])
lon_1_2 = (point_2['lon'] - point_1['lon'])

lat_2_3 = (point_3['lat'] - point_2['lat'])
lon_2_3 = (point_3['lon'] - point_2['lon'])

NUM_ROWS = 6 
NUM_COLS = 9 

coordinates = []

for i in range(0, NUM_ROWS):
    for j in range(0, NUM_COLS):
        lat = point_1['lat'] + (lat_1_2 / (NUM_ROWS-1)) * i + (lat_2_3 / (NUM_COLS-1)) * j
        lon = point_1['lon'] + (lon_1_2 / (NUM_ROWS-1)) * i + (lon_2_3 / (NUM_COLS-1)) * j
        coordinates.append((lat, lon))

with open("test.geojson", "w") as file:

    file.write('{\
  "type": "FeatureCollection",\n\
  "features": [\n')
    
    count = 1
    for i in range(0, len(coordinates)-(NUM_COLS)):
        if i == 0 or (i+1)%(NUM_COLS) != 0:
            str_to_write = f'{{\n\t"type":"Feature",\
            \n\t"properties": {{}},\
            \n\t"id": {count},\
            \n\t"geometry": {{\
                \n\t\t"type": "Polygon",\
                \n\t\t"coordinates": [\
                    \n\t\t\t[\
                    \n\t\t\t[\
                    \n\t\t\t\t{coordinates[i][1]},\
                    \n\t\t\t\t{coordinates[i][0]}\
                    \n\t\t\t],\
                    \n\t\t\t[\
                    \n\t\t\t\t{coordinates[i+1][1]},\
                    \n\t\t\t\t{coordinates[i+1][0]}\
                    \n\t\t\t],\
                    \n\t\t\t[\
                    \n\t\t\t\t{coordinates[i+NUM_COLS+1][1]},\
                    \n\t\t\t\t{coordinates[i+NUM_COLS+1][0]}\
                    \n\t\t\t],\
                    \n\t\t\t[\
                    \n\t\t\t\t{coordinates[i+NUM_COLS][1]},\
                    \n\t\t\t\t{coordinates[i+NUM_COLS][0]}\
                    \n\t\t\t],\
                    \n\t\t\t[\
                    \n\t\t\t{coordinates[i][1]},\
                    \n\t\t\t{coordinates[i][0]}\
                    \n\t\t\t]\
                    \n\t\t\t]\
                    \n\t\t]\
                    \n\t}}\
                    \n}}'
            file.write(str_to_write)
            count += 1
            if i != len(coordinates)-(NUM_COLS) - 2:
                file.write(',\n')
            else:
                file.write('\n')

    file.write(']\
            \n}')
    file.close()