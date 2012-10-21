#! /usr/bin/env python
import csv
import time
import numpy as np
#from pandas import *

filename = 'APC_Stops_Sept2012.txt'
keys = ['STOP_ID', 'STOP_NAME', 'ACT_STOP_TIME', 'ROUTE', 'LATITUDE', 'LONGITUDE', 'ACT_RUN_MINS', 'SCH_TIME']
outfile = 'sample-data.csv'

data = []
with open('data/%s' % filename, 'rt') as csv_file:
    reader = csv.DictReader(csv_file)
    for row in reader:
        filtered_row = {}
        for key in keys:
            filtered_row[key] = row[key]
        data.append(filtered_row)

tmp = []
for row in data:
    if row['ACT_RUN_MINS'] != '':
        tmp.append(row)

data = list(tmp)
del(tmp)


# epoch conversion
def time_to_epoch(ts):
    return time.mktime(time.strptime(ts, '%m/%d/%Y %I:%M:%S %p'))

tmp = []
for row in data:
    try:
        row['ACT_STOP_TIME_EPOCH'] = time_to_epoch(row['ACT_TIME'])  # '9/1/2012 7:46:00 AM'
        tmp.append(row)
    #except:
        # some timestamps are badly formed for some reason..
        #print 'badly formatted timestamp'

data = list(tmp)
del(tmp)

'''
data=sorted(data, key=lambda row: int(row['ACT_TIME_EPOCH']))
data=sorted(data, key=lambda row: int(row['STOP_SEQ_ID']))
data=sorted(data, key=lambda row: int(row['ROUTE']))
'''

# unique list of routes
routes = list(set([row['ROUTE'] for row in data]))
print routes


# lists of stops keyed by routes
stops = {}
'''
{
    '38': ['3094', '3049', ..]
    , '43': [...]
}
'''
for route in routes:
    stops[route] = []

for row in data:
    if row['STOP_ID'] not in stops[row['ROUTE']]:
        stops[row['ROUTE']].append(row['STOP_ID'])

''' compute headways
first store the epoch times in lists
these lists are keyed by stop IDs
those dictionaries are themselves keyed by routes
{
    route_a: {
        stop_1: [stamp1, stamp2]
        , stop_2: [...]
    }
    , route_b: { ...
    }
}
'''
# prepopulate the data structure
timestamps = {}
for route in stops.keys():
    if route == '0':
        continue
    timestamps[route] = {}
    for stop in stops[route]:
        timestamps[route][stop] = []


# appended all timestamps into the relevant 'bucket'
for row in data:
    if row['ROUTE'] == '0':
        continue
    timestamps[row['ROUTE']][row['STOP_ID']].append(int(row['ACT_STOP_TIME_EPOCH']))

# sorted the lists of timestamps
for route in timestamps.keys():
    for stop in timestamps[route].keys():
        timestamps[route][stop] = sorted(timestamps[route][stop])


''' computing headways
and write to the outfile csv
'''
headways = {}
for route in timestamps.keys():
    print "-------------------------------------------------"
    headways[route] = {}
    for stop in timestamps[route].keys():
        headways[route][stop] = {}
        tmpstop = []
        for i in range(len(timestamps[route][stop])): 
            if i == 0:
                continue
            if timestamps[route][stop][i] == timestamps[route][stop][i-1]:
                continue
            headway = (timestamps[route][stop][i] - timestamps[route][stop][i-1])/60
            tmpstop.append(headway)
            #print route, stop, headway
        headways[route][stop]["median"] = np.median(tmpstop)
        headways[route][stop]["vals"] = tmpstop
        print "------- %s\t%s\t%s ----- " % ( route, stop, headways[route][stop]["median"])

        '''
        for timestamp in timestamps[route][stop]:
            if timestamps[route][stop].index(timestamp) == 0:
                continue

            m = timestamps[route][stop].index(timestamp)
            headway = timestamps[route][stop][m] - timestamps[route][stop][m-1]
            headways.append(headway) '''
    tmplist = []
    for key,stop in headways[route].items():
        tmplist.append(stop["median"])
    headways[route]["median"] = np.median(tmplist)

    '''
    for key,stop in headways[route].items():
        stop["deltaMedian"] = []
        for val in stop["vals"]:
            stop["deltaMedian"].append(val-headway[route][
    '''
    headways[route]["median"] = np.median(tmplist)


    print "~~~~~~~~~~ %s\t%s ~~~~~~~ " % ( route,  headways[route]["median"])

#print float(sum(headways))/len(headways)


