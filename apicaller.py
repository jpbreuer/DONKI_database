# -*- coding: utf-8 -*-
"""
@author: jpbreuer
"""

import csv
import json
import datetime
#from bs4 import BeautifulSoup
#import urllib3
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

today = str(datetime.date.today())

###--- Coronal Mass Ejection (CME) --->
startDate = '1995-01-01'
endDate = today
mostAccurateOnly = 'true'
speed = '0'
halfAngle = '0'
catalog = 'ALL'

url = 'https://kauai.ccmc.gsfc.nasa.gov/DONKI/WS/get/CMEAnalysis?'
api = url + 'startDate=' + startDate + '&endDate=' + endDate + '&mostAccurateOnly=' + mostAccurateOnly + '&speed=' + speed + '&halfAngle=' + halfAngle + '&catalog=' + catalog

data = requests.get(api, verify=False).json()

f = csv.writer(open("CME_DONKI_database.csv","w"))
f.writerow(["Time21_5", "Latitude", "Longitude", "HalfAngle", "Speed", "Type", "AssociatedCMEID"])

for event in data:
    f.writerow([event["time21_5"],
                event["latitude"],
                event["longitude"],
                event["halfAngle"],
                event["speed"],
                event["type"],
                event["associatedCMEID"]])

###--- Geomagnetic Storm (GST) --->
startDate = '1995-01-01'
endDate = today

url = 'http://kauai.ccmc.gsfc.nasa.gov/DONKI/WS/get/GST?'
api = url + 'startDate=' + startDate + '&endDate=' + endDate

data = requests.get(api, verify=False).json()

f = csv.writer(open("GST_DONKI_database.csv","w"))
f.writerow(["GST ID", "Start Time", "Observed Time", "KP Index", "Source", "Linked Events Activity ID"])

for event in data:
    for ii in range(len(event["allKpIndex"])):
        if event["linkedEvents"] is None:
            f.writerow([event["gstID"],
                        event["startTime"],
                        event["allKpIndex"][ii]["observedTime"],
                        event["allKpIndex"][ii]["kpIndex"],
                        event["allKpIndex"][ii]["source"],
                        "None"])
        elif len(event["linkedEvents"]) > 1:
            activityIDs = ""
            for jj in range(len(event["linkedEvents"])):
                activityIDs += str(event["linkedEvents"][jj]["activityID"]) + ";"
            f.writerow([event["gstID"],
                        event["startTime"],
                        event["allKpIndex"][ii]["observedTime"],
                        event["allKpIndex"][ii]["kpIndex"],
                        event["allKpIndex"][ii]["source"],
                        activityIDs])
        else:
            f.writerow([event["gstID"],
                        event["startTime"],
                        event["allKpIndex"][ii]["observedTime"],
                        event["allKpIndex"][ii]["kpIndex"],
                        event["allKpIndex"][ii]["source"],
                        event["linkedEvents"][0]["activityID"]])

###--- Interplanetary Shock (IPS) --->
startDate = '1995-01-01'
endDate = today
location = 'ALL'
catalog = 'ALL'

url = 'http://kauai.ccmc.gsfc.nasa.gov/DONKI/WS/get/IPS?'
api = url + 'startDate=' + startDate + '&endDate=' + endDate + '&location=' + location + '&speed=' + '&catalog=' + catalog

data = requests.get(api, verify=False).json()

f = csv.writer(open("IPS_DONKI_database.csv","w"))
f.writerow(["IPS ID", "Event Time", "Location", "Instruments", "Catalog"])

for event in data:
    if len(event["instruments"]) > 1:
        instruments = ""
        for jj in range(len(event["instruments"])):
            instruments += str(event["instruments"][jj]["displayName"]) + ";"
        f.writerow([event["activityID"],
                    event["eventTime"],
                    event["location"],
                    instruments,
                    event["catalog"]])
    else:
        f.writerow([event["activityID"],
                    event["eventTime"],
                    event["location"],
                    event["instruments"][0]["displayName"],
                    event["catalog"]])

###--- Solar Flare (FLR) --->
startDate = '1995-01-01'
endDate = today

url = 'http://kauai.ccmc.gsfc.nasa.gov/DONKI/WS/get/FLR?'
api = url + 'startDate=' + startDate + '&endDate=' + endDate

data = requests.get(api, verify=False).json()

f = csv.writer(open("FLR_DONKI_database.csv","w"))
f.writerow(["Flare ID", "Begin Time", "Peak Time", "End Time", "Class Type","Source Location", "Active Region", "Instruments", "Linked Events Activity ID"])

for event in data:
    if event["linkedEvents"] is None:
        if len(event["instruments"]) > 1:
            instruments = ""
            for jj in range(len(event["instruments"])):
                instruments += str(event["instruments"][jj]["displayName"]) + ";"
            f.writerow([event["flrID"],
                    event["beginTime"],
                    event["peakTime"],
                    event["endTime"],
                    event["classType"],
                    event["sourceLocation"],
                    event["activeRegionNum"],
                    instruments,
                    "None"])
        else:
            f.writerow([event["flrID"],
                    event["beginTime"],
                    event["peakTime"],
                    event["endTime"],
                    event["classType"],
                    event["sourceLocation"],
                    event["activeRegionNum"],
                    event["instruments"][0]["displayName"],
                    "None"])

    elif len(event["instruments"]) > 1 or len(event["linkedEvents"]) > 1:
        instruments = ""
        activityIDs = ""
        for jj in range(len(event["instruments"])):
            instruments += str(event["instruments"][jj]["displayName"]) + ";"
        for jj in range(len(event["linkedEvents"])):
            activityIDs += str(event["linkedEvents"][jj]["activityID"]) + ";"
        f.writerow([event["flrID"],
                    event["beginTime"],
                    event["peakTime"],
                    event["endTime"],
                    event["classType"],
                    event["sourceLocation"],
                    event["activeRegionNum"],
                    instruments,
                    activityIDs])
    else:
        f.writerow([event["flrID"],
                    event["beginTime"],
                    event["peakTime"],
                    event["endTime"],
                    event["classType"],
                    event["sourceLocation"],
                    event["activeRegionNum"],
                    event["instruments"][0]["displayName"],
                    event["linkedEvents"][0]["activityID"]])

###--- Solar Energetic Particle (SEP) --->
startDate = '1995-01-01'
endDate = today

url = 'http://kauai.ccmc.gsfc.nasa.gov/DONKI/WS/get/SEP?'
api = url + 'startDate=' + startDate + '&endDate=' + endDate

data = requests.get(api, verify=False).json()

f = csv.writer(open("SEP_DONKI_database.csv","w"))
f.writerow(["SEP ID", "Event Time", "Instruments", "Linked Events Activity ID"])

for event in data:
    if event["linkedEvents"] is None:
        if len(event["instruments"]) > 1:
            instruments = ""
            for jj in range(len(event["instruments"])):
                instruments += str(event["instruments"][jj]["displayName"]) + ";"
            f.writerow([event["sepID"],
                    event["eventTime"],
                    instruments,
                    "None"])
        else:
            f.writerow([event["sepID"],
                    event["eventTime"],
                    event["instruments"][0]["displayName"],
                    "None"])

    elif len(event["instruments"]) > 1 or len(event["linkedEvents"]) > 1:
        instruments = ""
        activityIDs = ""
        for jj in range(len(event["instruments"])):
            instruments += str(event["instruments"][jj]["displayName"]) + ";"
        for jj in range(len(event["linkedEvents"])):
            activityIDs += str(event["linkedEvents"][jj]["activityID"]) + ";"
        f.writerow([event["sepID"],
                    event["eventTime"],
                    instruments,
                    activityIDs])
    else:
        f.writerow([event["sepID"],
                    event["eventTime"],
                    event["instruments"][0]["displayName"],
                    event["linkedEvents"][0]["activityID"]])

###--- Magnetopause Crossing (MPC) --->
startDate = '1995-01-01'
endDate = today

url = 'http://kauai.ccmc.gsfc.nasa.gov/DONKI/WS/get/MPC?'
api = url + 'startDate=' + startDate + '&endDate=' + endDate

data = requests.get(api, verify=False).json()

f = csv.writer(open("MPC_DONKI_database.csv","w"))
f.writerow(["MPC ID", "Event Time", "Instruments", "Linked Events Activity ID"])

for event in data:
    if event["linkedEvents"] is None:
        if len(event["instruments"]) > 1:
            instruments = ""
            for jj in range(len(event["instruments"])):
                instruments += str(event["instruments"][jj]["displayName"]) + ";"
            f.writerow([event["mpcID"],
                    event["eventTime"],
                    instruments,
                    "None"])
        else:
            f.writerow([event["mpcID"],
                    event["eventTime"],
                    event["instruments"][0]["displayName"],
                    "None"])

    elif len(event["instruments"]) > 1 or len(event["linkedEvents"]) > 1:
        instruments = ""
        activityIDs = ""
        for jj in range(len(event["instruments"])):
            instruments += str(event["instruments"][jj]["displayName"]) + ";"
        for jj in range(len(event["linkedEvents"])):
            activityIDs += str(event["linkedEvents"][jj]["activityID"]) + ";"
        f.writerow([event["mpcID"],
                    event["eventTime"],
                    instruments,
                    activityIDs])
    else:
        f.writerow([event["mpcID"],
                    event["eventTime"],
                    event["instruments"][0]["displayName"],
                    event["linkedEvents"][0]["activityID"]])

###--- Radiation Belt Enhancement (RBE) --->
startDate = '1995-01-01'
endDate = today

url = 'http://kauai.ccmc.gsfc.nasa.gov/DONKI/WS/get/RBE?'
api = url + 'startDate=' + startDate + '&endDate=' + endDate

data = requests.get(api, verify=False).json()

f = csv.writer(open("RBE_DONKI_database.csv","w"))
f.writerow(["RBE ID", "Event Time", "Instruments", "Linked Events Activity ID"])

for event in data:
    if event["linkedEvents"] is None:
        if len(event["instruments"]) > 1:
            instruments = ""
            for jj in range(len(event["instruments"])):
                instruments += str(event["instruments"][jj]["displayName"]) + ";"
            f.writerow([event["rbeID"],
                    event["eventTime"],
                    instruments,
                    "None"])
        else:
            f.writerow([event["rbeID"],
                    event["eventTime"],
                    event["instruments"][0]["displayName"],
                    "None"])

    elif len(event["instruments"]) > 1 or len(event["linkedEvents"]) > 1:
        instruments = ""
        activityIDs = ""
        for jj in range(len(event["instruments"])):
            instruments += str(event["instruments"][jj]["displayName"]) + ";"
        for jj in range(len(event["linkedEvents"])):
            activityIDs += str(event["linkedEvents"][jj]["activityID"]) + ";"
        f.writerow([event["rbeID"],
                    event["eventTime"],
                    instruments,
                    activityIDs])
    else:
        f.writerow([event["rbeID"],
                    event["eventTime"],
                    event["instruments"][0]["displayName"],
                    event["linkedEvents"][0]["activityID"]])

###--- High Speed Stream (HSS) --->
startDate = '1995-01-01'
endDate = today

url = 'http://kauai.ccmc.gsfc.nasa.gov/DONKI/WS/get/HSS?'
api = url + 'startDate=' + startDate + '&endDate=' + endDate

data = requests.get(api, verify=False).json()

f = csv.writer(open("HSS_DONKI_database.csv","w"))
f.writerow(["HSS ID", "Event Time", "Instruments", "Linked Events Activity ID"])

for event in data:
    if event["linkedEvents"] is None:
        if len(event["instruments"]) > 1:
            instruments = ""
            for jj in range(len(event["instruments"])):
                instruments += str(event["instruments"][jj]["displayName"]) + ";"
            f.writerow([event["hssID"],
                    event["eventTime"],
                    instruments,
                    "None"])
        else:
            f.writerow([event["hssID"],
                    event["eventTime"],
                    event["instruments"][0]["displayName"],
                    "None"])

    elif len(event["instruments"]) > 1 or len(event["linkedEvents"]) > 1:
        instruments = ""
        activityIDs = ""
        for jj in range(len(event["instruments"])):
            instruments += str(event["instruments"][jj]["displayName"]) + ";"
        for jj in range(len(event["linkedEvents"])):
            activityIDs += str(event["linkedEvents"][jj]["activityID"]) + ";"
        f.writerow([event["hssID"],
                    event["eventTime"],
                    instruments,
                    activityIDs])
    else:
        f.writerow([event["hssID"],
                    event["eventTime"],
                    event["instruments"][0]["displayName"],
                    event["linkedEvents"][0]["activityID"]])
