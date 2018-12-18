import requests, ast, time, threading, multiprocessing
from multiprocessing import Process
import paho.mqtt.client as paho
import socket
    
class Manager:
    # manager class, defines the means of communication for other objects and provides error checking and log-adding functions
    def __init__(self):
        with open('main_settings.sg', 'r') as f:
            r = f.read()
            ret = ast.literal_eval(r)
            self.main_settings = ret
            self.test_server = "google.com"

    def internet_connection_is_present(self):
    # check if internet connection is present by trying to connect to a test server
        try:
            host = socket.gethostbyname(self.test_server)
            s = socket.create_connection((host, 80), 2)
            return True
        except:
            pass
        return False
        
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
            self.update_settings()
            with open(self.main_settings['settings'], 'r') as f:
                r = f.read()
                try:
                    ret = ast.literal_eval(r)
                except:
                    self.add_log('002')
                    ret = 0
        return ret
    
    def update_settings(self):
        # update greenhouse settings from server
        if(self.internet_connection_is_present() is True):
            r = requests.get(url=self.main_settings['server']+'/api_GET.php?getSettings&greenhouse_id='+self.main_settings['greenhouse_id'])
            r = r.json()[0]
            with open(self.main_settings['settings'], 'w') as f:
                f.write(str(r))
            return r
        self.add_log('005')
        return "No internet connection"
    
    def update_error_codes(self):
    # update error codes from server
        if(Manager().internet_connection_is_present() is True):
            r = requests.get(url=self.main_settings['server']+'/api_GET.php?getErrorCodes')
            r = r.json()[0]
            with open(self.main_settings['error_codes'], 'w') as f:
                f.write(str(r))
            return r
        self.add_log('005')
        return "No Internet connection"
        
        

class Messanger:
    # this class establishes connection between objects and our server
   # def __init__(self):
       # self.connection_manager=Manager()
           
    def send_sensor_data_to_server(self,sensor_id, data):
        if(Manager().internet_connection_is_present() is True):
            print('sending...')
            date = int(time.time())
            r = requests.get(url = Manager().main_settings['server']+'/api_SET.php?setSensorData&sensor_id='+str(sensor_id)+'&data='+str(data)+'&date='+str(date))
            if(r.status_code == 200):
                return 1             
            else:
                Manager().add_log('003')
                return r.status_code
        else:
            Manager().add_log('005')
            return "No Internet connection"
            
            
    def send_relay_state_to_server(self,relay,state):
        if(Manager().internet_connection_is_present() is True):
            r = requests.get(url = Manager().main_settings['server']+'/api_SET.php?setRelayState&greenhouse_id='+Manager().main_settings['greenhouse_id']+'&state='+str(state))
            if(r.status_code == 200):
                return 1
            else:
                Manager().add_log('004')
                return r.status_code            
        else:
            Manager().add_log('005')
            return "No Internet connection"

class DataRetriever:
    # this class retrieves data from sensors and sends them to the server
    def __init__(self,name):
       # self.client_messanger = Messanger()
        self.broker = "localhost"
        self.client = paho.Client(name)
        self.subscribtion_list = []

    def add_basic_subscribtions(self):
        self.client.subscribe("moist/+")
        self.client.subscribe("hum/+")
        self.client.subscribe("temp/+")
        self.client.subscribe("light/+")
        self.client.subscribe("co2/+")
        self.subscribtion_list = [ "moist/", "hum/", "temp/", "light/", "co2/" ]

    def add_subscribtion(self,topic):
        self.client.subscribe(topic)
        self.subscribtion_list.append(topic)

    def is_subscribed_to(self, topic):
        for subscribtions in self.subscribtion_list:
            if(subscribtions==topic):
                return True
        return False

    def get_id_token(self,subscribtion):
    # the sensor's id is published at the end of the topic, after the '/' sign
        for token in range(0,len(subscribtion)):
            if(subscribtion[token]=='/'):
                return 1+token

    def get_sender_id(self,from_topic):
    # so we get to the '/' character and return everything ahead of it as sensor's id
        return from_topic[self.get_id_token(from_topic):]

    def on_message(self, client, userdata, message):
    # DataRetriever sends every bit of data it gets to the server
        if(self.is_subscribed_to(message.topic[:-1])):
            Messanger().send_sensor_data_to_server(self.get_sender_id(str(message.topic)),int(message.payload))
           
    def establish_connection(self):
    # the on_message field of mqtt paho's client is a function that is invoked when the client recieves publication from a topic it is subscribed to
    # important: add subscription topics after establishing connection
        self.client.on_message=self.on_message
        self.client.connect(self.broker)

    def start_retrieving_data(self):
    # loops up to the point of the end of program's execution, constantly looking for publications
        self.client.loop_start()

class DataProcessor:
    #this class processes the data from sensors and acts according to  the settings
    def __init__(self,name):
        self.broker = "localhost"
        self.client = paho.Client(name)
        self.subscribtion_list = []
        self.data_settings=Manager().read_settings()
        self.sender_id = -1
        self.sent_data = -1

    def update_data_settings(self):
        self.data_settings=Manager().read_settings()

    def add_basic_subscribtions(self):
        self.client.subscribe("moist/+")
        self.client.subscribe("hum/+")
        self.client.subscribe("temp/+")
        self.client.subscribe("light/+")
        self.client.subscribe("co2/+")
        self.subscribtion_list = [ "moist/", "hum/", "temp/", "light/", "co2/" ]

    def add_subscribtion(self,topic):
        self.client.subscribe(topic)
        self.subscribtion_list.append(topic)

    def is_subscribed_to(self, topic):
        for subscribtions in self.subscribtion_list:
            if(subscribtions==topic):
                return True
        return False

    def get_id_token(self,subscribtion):
        for token in range(0,len(subscribtion)):
            if(subscribtion[token]=='/'):
                return 1+token

    def get_sender_id(self,from_topic):
        return from_topic[self.get_id_token(from_topic):]

    def turn_on(self,relay):
        Messanger().send_relay_state_to_server(relay,'1')
        self.client.publish('control', str(relay)+'1')

    def turn_off(self,relay):
        Messanger().send_relay_state_to_server(relay,'0')
        self.client.publish('control', str(relay)+'0')

    def process_data(self):
    # relay 1 corresponds to the watering system, relay 2 corresponds to the infrared lights, relay three controls the average lights and relay 4 controls the cooler 
        if(self.sender_id==1):
        # get the id of the publisher and act according to the given settings
            if(self.sent_data < int(self.data_settings['moist_min'])):
                self.turn_on(1)
            if(self.sent_data > int(self.data_settings['moist_max'])):
               self.turn_off(1)
        if(self.sender_id==2):
            if(self.sent_data < int(self.data_settings['temp_min'])):
                self.turn_on(2)
                self.turn_off(4)
            if(self.sent_data > int(self.data_settings['temp_max'])):
                self.turn_on(4)
                self.turn_off(2)
        if(self.sender_id==4):
            if(self.sent_data < int(self.data_settings['light_min'])):
                self.turn_on(3)
            if(self.sent_data > int(self.data_settings['light_max'])):
                self.turn_off(3)
        pass

    def on_message(self, client, userdata, message):
        self.update_data_settings() # update settings before processing data
        print('processing...')
        if(self.is_subscribed_to(message.topic[:-1])):
            self.sender_id = int(self.get_sender_id(str(message.topic)))
            self.sent_data = int(message.payload)
            self.process_data()

    def establish_connection(self):
        self.client.on_message=self.on_message
        self.client.connect(self.broker)

    def start_processing_data(self):
        self.client.loop_start()

# Basically, both DataRetriever and DataProcessor get data from sensors and do something with them and ideally there should've been an abstract class GetData from which both classes inherit
# but we decided to omit inheritance to not damage the program's performance

class BackgroundUpdateChecker:
    # checks for updates in the background
    # Important: Prefer Process class to the Thread class in Threading module to maximize the CPU's performance
    def __init__(self, interval=3600):
        self.interval = interval
        #self.update_manager=Manager()
        self.process = Process(target=self.run, args=())
        self.process.start()
        
        
    def run(self):
        while True:
            print('updating settings...')
            #self.update_manager.update_settings()
            Manager().update_settings()
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
#manager = Manager()            
#messanger = Messanger()
         
#def on_message(client, userdata, message):
#    print(str(message.topic[6:]),' : ',str(message.payload))
#    messanger.send_sensor_data_to_server(int(message.topic[6:]),int(message.payload))

#def add_subscribtions(client):
#    client.subscribe("moist/+")
#    client.subscribe("hum")
#    client.subscribe("temp")
#    client.subscribe("light")
#    client.subscribe("co2")
        #client.subscribe("ph")
        #client.subscribe("ec")
        #client.subscribe("wijndSpeed")
        #client.subscribe("windDir")

def main():
   # print("starting the main thread and loading the settings")
   # print("launch anything you need from here")
   # manager=Manager()
   # messanger=Messanger()
   # broker="localhost"
    #client= paho.Client("main")
    #client.on_message=on_message
    
    #client.connect(broker)
    #client.loop_start()
    #add_subscribtions(client)

    bguc=BackgroundUpdateChecker(60)
    data_retriever = DataRetriever("main")
    data_retriever.establish_connection()
    data_retriever.add_basic_subscribtions()
    data_retriever.start_retrieving_data()
    data_processor = DataProcessor('client_001')
    data_processor.establish_connection()
    data_processor.add_basic_subscribtions()
    data_processor.start_processing_data()
    #bgsc=BackgroundSensorChecker(5)   
    while True: 
       print('press q to exit')
       a=input()
       if(a=='q'):
           #bgsc.process.terminate()
           bguc.process.terminate()
           break
 
if __name__ == '__main__': # don't touch this line
    main()
