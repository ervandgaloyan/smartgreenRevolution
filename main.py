#!/usr/bin/env python3

import requests, ast, time

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
    #print(ms['server']+'/api_SET.php?setSystemLog&importance=0&greenhouse_id='+ms['greenhouse_id']+'&customer_id=1'+'&log='+str(log)+'&code='+code)

    # send error to server
    r = requests.get(url=ms['server']+'/api_SET.php?setSystemLog&importance=0&greenhouse_id='+ms['greenhouse_id']+'&customer_id=1'+'&log='+str(log)+'&code='+code)
    if(r.status_code == 200):
        return 1
    else:
        return r.status_code

def send_data(data, sensor_id):
    date = int(time.time())
    r = requests.get(url=ms['server']+'/api_SET.php?setSensorData&sensor_id='+str(sensor_id)+'&data='+str(data)+'&date='+str(date))
    if(r.status_code == 200):
        return 1
    else:
        return r.status_code
ms = read_main_settings()
print(update_error_codes())
#update_settings()
#settings = read_settings()
#print(settings)
#print(settings['moist_max'])
#add_log('000')
#print(update_error_codes())
#print(send_data(65,1))
