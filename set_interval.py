from threading import Timer

import requests




def update_data():
    greenhouseinfo = requests.get(url = ms['server'] + '/api_GET.php?greenhouse_id=' + ms['greenhouse_id'])
    sensorid = requests.get(url = ms['server']+'/api_GET.php?sensor_id')
    #sensorinfo = requests.get(url = ms['server']+'/api_GET.php?getSensorInfo')
    sensordata = requests.get(url = ms['server']+'/api_GET.php?getSensorData')
    f = 'Data from greenhouse number '  str(greenhouse_id)+'s sensor number' + str(sensorid) + ': '  + str(sensordata)
    t = Timer(3600.0, update_data)
    t.start()
    print(f)    
    
def start_updating_data():
    Timer(1.0,update_data).start()
   
    

start_updating_data()
