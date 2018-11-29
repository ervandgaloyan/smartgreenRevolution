import requests, ast, time, threading, multiprocessing
from multiprocessing import Process
import paho.mqtt.client as paho
    
class Manager:
    
    def __init__(self):
        with open('main_settings.sg', 'r') as f:
            r = f.read()
            ret = ast.literal_eval(r)
            self.main_settings=ret
        
    def add_log(self,code, type = ' ', log = ' ' ):
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
            with open(self.main_settings['log'], 'a') as f:
                f.write(type + ": " + log + ", time: " + str(int(time.time())) + ", Code: " + code + "\n")

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
           
    def send_sensor_data_to_server(self,sensor_id, data):
        date = int(time.time())
        r = requests.get(url=self.connection_manager.main_settings['server']+'/api_SET.php?setSensorData&sensor_id='+str(sensor_id)+'&data='+str(data)+'&date='+str(date))
        print(self.connection_manager.main_settings['server']+'/api_SET.php?setSensorData&sensor_id='+str(sensor_id)+'&data='+str(data)+'&date='+str(date))
        if(r.status_code == 200):
            return 1             
        else:
            connection_manager.add_log('003')
            return r.status_code
            
    def send_relay_state_to_server(self,relay,state):
        r=requests.get(url=self.connection_manager.main_settings['server']+'/api_SET.php?setRelayState&greenhouse_id='+self.connection_manager.main_settings['greenhouse_id']+'&state='+str(state))
        if(r.status_code == 200):
            return 1
        else:
            connection_manager.add_log('004')
            return r.status_code            

class DataRetriever:
    def __init__(self):
        self.client_messenger = Messenger()
        self.broker = "localhost"
        self.client = paho.Client("main")
        self.subscription_list = []

    def add_basic_subscribtions(self):
        self.client.subscribe("moist")
        self.client.subscribe("hum")
        self.client.subscribe("temp")
        self.client.subscribe("light")
        self.client.subscribe("co2")
        self.subscription_list = [ "moist", "hum", "temp", "light", "co2" ]

    def add_subscription(self,topic):
        self.client.subscribe(topic)
        self.subscription_list.append(topic)

    def is_subscribed_to(self, topic):
        for subscriptions in self.subscription_list:
            if(subscriptions==topic):
                return True
        return False

    def catch_and_send_data(self, client, userdata, message):
        print(str(message.topic),' : ', int(message.payload))
        if(self.is_subscribed_to(message.topic)):
            self.client_messenger.send_sensor_data_to_server(client,messege.payload)
            print(str(message.topic),' : ', int(message.payload))

    def establish_connection(self):
        self.client.on_message=self.catch_and_send_data
        self.client.connect(self.broker)

    def start_retrieving_data(self):
        self.client.loop_start()

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
    

    
    
#class BackgroundSensorChecker:
#    def __init__(self,interval=900):
#        pass
#        self.interval = interval
#        self.process = Process(target=self.run, args=())
#        self.process.start()
        
    
#    def run(self):
#        while True:
#            print('checking the sensors...')
#            time.sleep(self.interval)
            
         
 

def main():
    print("starting the main thread and loading the settings")
    print("launch anything you need from here")
    manager = Manager()
    messenger = Messenger()
    bguc=BackgroundUpdateChecker(6)
    data_retriever = DataRetriever()
    data_retriever.add_basic_subscribtions()
    data_retriever.establish_connection()
    data_retriever.start_retrieving_data()
    
    #bgsc=BackgroundSensorChecker(5)   
    while True: 
      # data_retriever.start_retrieving_data()
       print('press q to exit')
       a=input()
       if(a=='q'):
           #bgsc.process.terminate()
           bguc.process.terminate()
           break
 
if __name__ == '__main__':
    main()
