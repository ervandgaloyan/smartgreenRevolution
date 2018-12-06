#!/usr/bin/env python3

from json import dumps
from time import time
from ast import literal_eval

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
            ret = ast.literal_eval(r)
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
            ret = ast.literal_eval(r)
        return ret
    
    def notification_write(self, importance, notification, customer_id, date):
        add = {'importance': importance, 'notification': notification, 'customer_id': customer_id, 'date': date}
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

    def sensor_data_write(self,data,dataFile):
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
            ret = ast.literal_eval(r)
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
            ret = ast.literal_eval(r)
        return ret

    def system_log_write(self, type = ' ', log = ' ' ):
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
        with open(self.ms['log'], 'a') as f:
            f.write(",{" + type + ": " + log + ", time: " + str(int(time.time())) + ", Code: " + code + "}")

    def system_log_read(self):
        with open(self.ms['log'], "r") as f:
            r = f.read()
            r = '['+ r + ']'
            data = literal_eval(r)
        return data
