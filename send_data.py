#!/usr/bin/env python3
import requests, time

def send_data(data, sensor_id):
    date = int(time.time())
    print('https://av-royaldecor.com/sg/api_SET.php?setSensorData&sensor_id='+str(sensor_id)+'&data='+str(data)+'&date='+str(date))
    return requests.get(url='https://av-royaldecor.com/sg/api_SET.php?setSensorData&sensor_id='+str(sensor_id)+'&data='+str(data)+'&date='+str(date))

print(send_data(96,2))

