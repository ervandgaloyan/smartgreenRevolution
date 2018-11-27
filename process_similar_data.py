#!/usr/bin/env python3

from statistics import median, mean

def process_similar_data(data,per):
    # data -> array from 1 to 100
    # per -> percent

    data.sort()
    length = len(data)

    for x in range(int(length/2)):
        med = float(median(data[x+1:]))
        if(data[x] < med-per):
            data = data[x+1:]
        else:
            break
    length = len(data)
    for x in range(length-1, int(length/2),-1):
        med = float(median(data[:x]))
        if(data[x] > med+per):
            data = data[:x]
        else:
            break
    print(data)
    return int(mean(data))

data = [50,60,70,1,2,3,56,55,44,99,100]
print(process_similar_data(data,40))
