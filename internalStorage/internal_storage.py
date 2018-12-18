#!/usr/bin/env python3

from json import dumps
from time import time
from ast import literal_eval
import requests

class Internal_Storage:
    def __init__(self, ms):
        self.ms = ms

    def error_codes_write(self):
        r = requests.get(url=self.ms['server']+'/api_GET.php?getErrorCodes')
        r = r.json()
        with open(self.ms['error_codes'], 'w') as f:
            f.write(str(r))
        return r

    def error_codes_read(self):
        with open(self.ms['error_codes'], 'r') as f:
            r = f.read()
            ret = literal_eval(r)
        return ret

    def greenhouse_write(self):
        r = requests.get(url=self.ms['server']+'/api_GET.php?getGreenhouseInfo&greenhouse_id='+self.ms['greenhouse_id'])
        r = r.json()
        with open(self.ms['greenhouse'], 'w') as f:
            f.write(str(r))
        return r

    def greenhouse_read(self):
        with open(self.ms['greenhouse'], 'r') as f:
            r = f.read()
            ret = literal_eval(r)
        return ret

    def notification_write(self, importance, notification, customer_id, date):
        add = {'importance': str(importance), 'notification': str(notification), 'customer_id': str(customer_id), 'date': str(date)}
        with open(self.ms['notification'], "r") as f:
            r = f.read()
            data = literal_eval(r)

        data.append(add)

        with open(self.ms['notification'], "w") as f:
            f.write(dumps(data))
        return 1

    def notification_read(self):
        with open(self.ms['notification'], "r") as f:
            r = f.read()
            data = literal_eval(r)
        return data

    def relay_write(self, relay_id, state, time):
        add = {'relay_id': relay_id, 'state': state, 'time': time}
        with open(self.ms['relay'], "r") as f:
            r = f.read()
            data = literal_eval(r)

        data.append(add)

        with open(self.ms['relay'], "w") as f:
            f.write(dumps(data))
        return 1

    def relay_read(self):
        with open(self.ms['relay'], "r") as f:
            r = f.read()
            data = literal_eval(r)
        return data

    def sensor_data_write(self,sensor_id,data,dataFile):
        with open(dataFile, "a") as f:
            f.write(', ' + dumps([sensor_id, data, int(time())]))
        return 1

    def sensor_data_read(self,dataFile):
        with open(dataFile, "r") as f:
            r = f.read()
            r = '['+ r + ']'
            data = literal_eval(r)
        return data

    def sensor_list_write(self):
        r = requests.get(url=self.ms['server']+'/api_GET.php?getSensorInfo&greenhouse_id='+self.ms['greenhouse_id'])
        r = r.json()
        with open(self.ms['sensor_list'], 'w') as f:
            f.write(str(r))
        return r

    def sensor_list_read(self):
        with open(self.ms['sensor_list'], 'r') as f:
            r = f.read()
            ret = literal_eval(r)
        return ret

    def settings_write(self):
        r = requests.get(url=self.ms['server']+'/api_GET.php?getSettings&greenhouse_id='+self.ms['greenhouse_id'])
        r = r.json()[0]
        with open(self.ms['settings'], 'w') as f:
            f.write(str(r))
        return r

    def settings_read(self):
        with open(self.ms['settings'], 'r') as f:
            r = f.read()
            ret = literal_eval(r)
        return ret

ms = {'server': 'http://smartgreen.cc/demo/api', 'greenhouse_id': '1', 'greenhouse': 'greenhouse.sg', 'settings': 'settings.sg', 'error_codes': 'error_codes.sg', 'log': 'log.sg', 'updated': 'updated.sg', 'notification': 'notification.sg', 'relay': 'relay.sg', 'sensor_list': 'sensor_list.sg'}
IS = Internal_Storage(ms)

#IS.error_codes_write()
#print(IS.error_codes_read())

#IS.greenhouse_write()
#print(IS.greenhouse_read())

#IS.notification_write(1,'rgrdgdrdrgt',1,44787787)
#print(IS.notification_read())

#IS.relay_write('RW2',1,5554455)
#print(IS.relay_read())

#IS.sensor_data_write(5,68, 'moist_data.sg')
#print(IS.sensor_data_read('moist_data.sg'))

#IS.sensor_list_write()
#print(IS.sensor_list_read())

#IS.settings_write()
#print(IS.settings_read())


