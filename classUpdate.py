#!/usr/bin/env python3

import requests, ast, time

class Update:

    def __init__(self, server, greenhouse_id, error_codes, settings, updated):
        self.greenhouse_id = greenhouse_id
        self.server = server
        self.error_codes = error_codes
        self.settings = settings
        self.updated = updated
        self.last_time = self.get_last_time()
        print(self.last_time)
        self.check()

    def get_last_time(self):
        with open(self.updated, 'r') as f:
            r = f.read()
            try:
                ret = ast.literal_eval(r)['settings']
            except:
                ret = 0
        return ret

    def set_last_time(self):
        with open(self.updated, 'r') as f:
            r = f.read()
            ret = ast.literal_eval(r)
            ret['settings'] = int(time.time())

        with open(self.updated, 'w') as f:
            f.write(str(ret))
        return 1

    def check(self):
        r = requests.get(url=self.server+'/api_GET.php?checkUpdate&greenhouse_id='+self.greenhouse_id+'&last_update='+str(self.last_time))
        r = r.json()[0]
        if(r == 1):
            self.update_settings()
            self.update_error_codes()
        self.set_last_time()

    def update_settings(self):
        # update greenhouse settings via server
        r = requests.get(url=self.server+'/api_GET.php?getSettings&greenhouse_id='+self.greenhouse_id)
        r = r.json()[0]
        with open(self.settings, 'w') as f:
            f.write(str(r))
        return r

    def update_error_codes(self):
        r = requests.get(url=self.server+'/api_GET.php?getErrorCodes')
        r = r.json()
        with open(self.error_codes, 'w') as f:
            f.write(str(r))
        return r

up = Update('http://smartgreen.cc/demo/api', '1', 'error_codes.sg', 'settings.sg','updated.sg')

