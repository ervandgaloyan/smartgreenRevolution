#!/usr/bin/env python3

from json import dumps
from time import time
from ast import literal_eval

class Internal_data:
    def __init__(self, dataFile):
        self.dataFile = dataFile

    def save_data(self, sensor_id, data):
        with open(self.dataFile, "a") as f:
            f.write(', ' + dumps([sensor_id, data, int(time())]))

    def remove_data(self,date):
        data = []
        with open(self.dataFile, "r") as f:
            r = f.read()
            r = '['+ r + ']'
            data = literal_eval(r)
        newData = data
        print(newData)

        while True:
            if(newData[0][2] < date):
                newData.pop(0)
            else:
                break
        print(newData)
        with open(self.dataFile, "w") as f:
            f.write(dumps(newData)[1:-1])

a = Internal_data('moisture_data.sg')
#a.save_data(1,65)
a.remove_data(1543412661)
