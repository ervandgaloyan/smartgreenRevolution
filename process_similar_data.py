#!/usr/bin/env python3

import statistics

def process_similar_data(data):
    data.sort()
    mediana = statistics.median(data)
    for x in data:
        
