# -*- coding: utf-8 -*-
"""
Created on Tue Apr 22 12:24:30 2025

@author: julia
"""

import blpapi
from blpapi import SessionOptions, Session, Service
import pandas as pd
import time
import numpy as np
#%%


fields = ['CPR-MTD', 'CPR-LTD', 'YLD_YTM_MID']

#bloomberg session setup
options = SessionOptions()
options.setServerHost('localhost')
options.setServerPort(8194)

session = Session(options)

if not session.start():
    print('Failed to start session')
    exit()

if not session.openService("//blp//refdata"):
    print("Failed to open //blp/refdata")
    exit()

refDataService = session.getService("//blp/refdata")
request = refDataService.createRequest("ReferenceDataRequest")

#%% add securities and fields
cusip_list = pd.read_csv(r"C:\Users\julia\OneDrive\Documents\CUSIPsYields.xlsx")

for cusip in cusip_list:
    request.append("securities", cusip)
request.append("fields", field)

#send request
session.sendRequest(request)

#process response
results = []

for field in fields:
    ev = session.nextEvent()
    for msg in ev:
        if msg.hasElement("securityData"):
            sec = security.getElementAsString("security")
            if security.hasElement("fieldData"):
                data = security.getElement("fieldData")
                cpr = data.getElementAsFloat(field) 
        if data.hasElement(field):
            else None
                results.append((sec, cpr))
    if ev.eventType() == blpapi.Event.RESPONSE:
        break
    
#%% convert to dataframe
df = pd.DataFrame(results, columns = ['CUSIP', fields])
print(df)

#%% save to excel

df.to_excel("bloomberg_data.xlsx", index = False)
