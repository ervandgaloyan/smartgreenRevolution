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
            log = 'Not registred the error code'
    with open(ms['log'], 'a') as f:
        f.write(type + ": " + log + ", time: " + str(int(time.time())) + ", Code: " + code + "\n")

    # send error to server
    # requests.get(url=ms['server']+'/api_GET.php?setError&greenhouse_id='+ms['greenhouse_id'])


ms = read_main_settings()
#update_settings()
#settings = read_settings()
#print(settings)
#print(settings['moist_max'])
#add_log("Error","test test","001")
print(update_error_code())
