import requests, ast, time

def add_log(code, type = ' ', log = ' ' ):
    # add error to file & send to the server via api
    if(code != '000'):
        try:
            type = error_codes[code][type]
            log = error_codes[code][log]
        except:
            type = 'Error'
            log = 'Undefined Error'
    else:
        type = 'Error'
        log = 'Not registred the error code'
    with open(ms['log'], 'a') as f:
        f.write(type + ": " + log + ", time: " + str(int(time.time())) + ", Code: " + code + "\n")
        
class Messanger:
    def __init__(self,adress):
        self.server_adress=adress
	   
    def send_sensor_data_to_server(self,data,sensor_id):
        try:
            date = int(time.time())
            r = requests.get(url=self.server_adress+'/api_SET.php?setSensorData&sensor_id='+str(sensor_id)+'&data='+str(data)+'&date='+str(date))
            if(r.status_code == 200):
                return 1
            else:
                return r.status_code
	except:
            add_log('003')
			
    def send_relay_status_to_server(self,relay,status):
	pass
