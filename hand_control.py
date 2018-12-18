import time
import paho.mqtt.client as paho
broker="localhost"
arrived = 0

def on_message(client, userdata, message):
    time.sleep(1)
    print("received message =",str(message.topic))

client= paho.Client("client-001")
client.on_message=on_message

print("connecting to broker ",broker)
client.connect(broker)#connect
client.loop_start() #start loop to process received messages

#print("subscribing ")
def control(relay,state):
    global arrived
    loops = 0
    client.publish('control',str(relay)+str(state))
    return 1
    while(arrived==0):
        time.sleep(0.1)
        loops += 1
        if(loops == 50):
            print("Error: didn't arrive")
            return 0
    return 1
#client.subscribe("control")
#time.sleep(2)
#control(5,0)
#print("publishing ")
#client.publish("house/bulb1","on")#publish
#time.sleep(4)
while(True):
    print('1 : Pump | 2 : IR | 3 : Cooler | 4 : Light | 5 : Window | 0 to exit')
    read = input('Example "40"')
    if(read == '0'):
        break
    relay = int(read[0])
    state = int(read[1])
    control(relay, state)
client.disconnect() #disconnect
client.loop_stop() #stop loop
