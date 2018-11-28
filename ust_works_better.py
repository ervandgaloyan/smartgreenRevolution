import requests, ast, time, threading, multiprocessing
from multiprocessing import Process

def read_main_settings():
    # read main settings from file main_settings.sg
    with open('main_settings.sg', 'r') as f:
        r = f.read()
        try:
            ret = ast.literal_eval(r)
        except:
            self.add_log("001")
            ret = 0
        return ret
    
    
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
            
            
class Manager:
    
    def __init__(self):
        self.main_settings=read_main_settings()
        
    def read_settings(self):
    #read greenhouse settings from file
        f = open(self.main_settings['settings'], 'r')
        r = f.read()
        try:
            ret = ast.literal_eval(r)
        except:
            f.close()
            update_settings()
            with open(self.main_settings['settings'], 'r') as f:
                r = f.read()
                try:
                    ret = ast.literal_eval(r)
                except:
                    self.add_log('002')
                    ret = 0
        return ret  
    
    def update_settings(self):
    # update greenhouse settings via server
        r = requests.get(url=self.main_settings['server']+'/api_GET.php?getSettings&greenhouse_id='+self.main_settings['greenhouse_id'])
        r = r.json()[0]
        with open(self.main_settings['settings'], 'w') as f:
            f.write(str(r))
        return r
    
    def update_error_codes(self):
        r = requests.get(url=self.main_settings['server']+'/api_GET.php?getErrorCodes')
        r = r.json()[0]
        with open(self.main_settings['error_codes'], 'w') as f:
            f.write(str(r))
        return r
        
        

class Messenger:
    def __init__(self):
        self.connection_manager=Manager()
           
    def send_sensor_data_to_server(self,data,sensor_id):
        date = int(time.time())
        r = requests.get(url=self.connection_manager.ms['server']+'/api_SET.php?setSensorData&sensor_id='+str(sensor_id)+'&data='+str(data)+'&date='+str(date))
        if(r.status_code == 200):
            return 1             
        else:
            add_log('003')
            return r.status_code
            
    def send_relay_state_to_server(self,relay,state):
        r=requests.get(url=self.connection_manager.main_settings['server']+'/api_SET.php?setRelayState&greenhouse_id='+self.connection_manager.main_settings['greenhouse_id']+'&state='+str(state))
        if(r.status_code == 200):
            return 1
        else:
            add_log('004')
            return r.status_code            

class BackgroundUpdateChecker:
    def __init__(self, interval=3600):
        self.interval = interval
        self.update_manager=Manager()
        self.process = Process(target=self.run, args=())
        self.process.start()
        
        
    def run(self):
        while True:
            print('updating settings...')
            self.update_manager.update_settings()
            time.sleep(self.interval)           
    
class DataRetriever:
    def __init__(self,sensor_list,relay_list):
        pass
    
    def get_relay_status(self,relay):
        pass
    
    def get_sensor_data(self,sensor):
        pass       

class RelayController:
    def __init__(self,relay_list):
        pass
    
    def set_relay_on(self,relay):
        pass
    
    def set_relay_off(self,relay):
        pass

    def check_sensor(self,sensor):
        pass
        #if something: set_relay_on(some_relay)
        #if something_else: set_relay_off(some_other_relay)
    
    
class BackgroundSensorChecker:
    def __init__(self,interval=900):
        pass
        self.interval = interval
        self.process = Process(target=self.run, args=())
        self.process.start()
        
    
    def run(self):
        while True:
            print('checking the sensors...')
            time.sleep(self.interval)
            
         
 

def main():
    print("starting the main thread and loading the settings")
    print("launch anything you need from here")
    messenger=Messenger()
    bguc=BackgroundUpdateChecker(2)
    bgsc=BackgroundSensorChecker(5)   
    while True: 
       print('press q to exit')
       a=input()
       if(a=='q'):
           bgsc.process.terminate()
           bguc.process.terminate()
           break
            
ms=read_main_settings() 
if __name__ == '__main__':
    main()
