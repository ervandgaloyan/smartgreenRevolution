import requests, ast, time

def read_main_settings():
    # read main settings from file main_settings.sg
    with open('main_settings.sg', 'r') as f:
        r = f.read()
        try:
            ret = ast.literal_eval(r)
        except:
            add_log("001")
            ret = 0
    return ret

def update_settings():
        # update greenhouse settings via server
        r = requests.get(url=ms['server']+'/api_GET.php?getSettings&greenhouse_id='+ms['greenhouse_id'])
        r = r.json()[0]
        with open(ms['settings'], 'w') as f:
            f.write(str(r))
        return r

def read_settings():
    #read greenhouse settings from file
    f = open(ms['settings'], 'r')
    r = f.read()
    try:
        ret = ast.literal_eval(r)
    except:
        f.close()
        update_settings()
        with open(ms['settings'], 'r') as f:
            r = f.read()
            try:
                ret = ast.literal_eval(r)
            except:
                add_log('002')
                ret = 0
    return ret

def update_error_codes():
    r = requests.get(url=ms['server']+'/api_GET.php?getErrorCodes')
    r = r.json()[0]
    with open(ms['error_codes'], 'w') as f:
        f.write(str(r))
    return r

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
    def __init__(self):
        self.main_data=read_main_settings()
           
    def send_sensor_data_to_server(self,data,sensor_id):
        try:
            date = int(time.time())
            r = requests.get(url=self.main_data['server']+'/api_SET.php?setSensorData&sensor_id='+str(sensor_id)+'&data='+str(data)+'&date='+str(date))
            if(r.status_code == 200):
                return 1             
	except:
            add_log('003')
            return r.status_code
			
    def send_relay_status_to_server(self,relay,status):
	try:
            r=requests.get(url=self.main_data['server']+'/api_SET.php?setRelayState&greenhouse_id='+self.main_data['greenhouse_id']+'&state='+str(state))
            if(r.status_code == 200):
                return 1
        except:
            add_log('004')
            return r.status_code
	
class BackgroundUpdateChecker(object):
    def __init__(self, interval=3600):
        self.interval = interval
	self.main_data=read_main_settings()
        thread = threading.Thread(target=self.run, args=())
        thread.daemon = True #prevents from joining
        thread.start()
        
#    def update_settings():
       # update greenhouse settings via server
#        r = requests.get(url=self.main_data['server']+'/api_GET.php?getSettings&greenhouse_id='+self.main_data['greenhouse_id'])
#        r = r.json()[0]
#        with open(self.main_data['settings'], 'w') as f:
#            f.write(str(r))
#        return r
	
    def run(self):
        while True:
            update_settings()
            time.sleep(self.interval)
		
class DataRetriever:
    def __init__(self,sensor_list,relay_list):
        self.sensors = sensor_list
	self.relays = relay_list
	
    def get_relay_status(self,relay):
	pass
    
    def get_sensor_data(self,sensor):
        pass       

class RelayController:
    def __init__(self,relay_list):
	self.relays = relay_list
	
    def set_relay_on(self,relay):
	pass
    
    def set_relay_off(self,relay):
	pass

    def check_sensor(self,sensor):
	pass
        #if something: set_relay_on(some_relay)
        #if something_else: set_relay_off(some_other_relay)
	
	
class BackgroundSensorCheck(DartaRetriever):
	def __init__(self,sensor_list,relay_list,interval=900):
	    super.__init__(sensor_list,relay_list)
	    self.interval = interval
            thread = threading.Thread(target=self.run, args=())
            thread.daemon = True #prevents from joining
            thread.start()
	
	def run_full_sensor_check():
	    relay_controller=RelayController(self.relays)
	    for s in self.sensors:
		relay_controller.check_sensor(s)
		
	def run():
	    while True:
	        self.run_full_sensor_check()
		time.sleep(self.interval)
		
		
ms=read_main_settings()
#update_checker=BackgroundUpdateChecker()
#messenger=Messenger()
#messenger.send_sensor_data_to_server(60,1)
#messanger.send_relay_status_to_server('RW1',1)
#while True:
#    print('input <Exit> to end the program')
#    a=input()
#    if(a=='Exit'):
#        break
