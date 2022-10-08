

# Why do we do this?
# To obtain data at the a certain resolution from Google Trends,
# it must be requested in batches (for example, 1-hour data
# needs to be requested in 7-day intervals).
# However, the values that the Trends API returns are scaled
# from 0-100 within that batch, so it is impossible to compare
# data points from different batches.
# This script re-scales the data by requesting batches with
# overlapping time periods.


## SETUP ##
from datetime import datetime, timedelta
import pandas as pd
import os
import sys
import time

daily = False  
hourly = False
weekly = False


path = '.'
os.chdir(path)
filename = 'bitcoin.csv'

if len(sys.argv) != 2:
    print("Usage: python scaledata.py <hourly/daily>")
    exit(-1)
elif sys.argv[1] == 'hourly':
    hourly = True
    filename = 'bitcoin_hourly.csv'
elif sys.argv[1] == 'daily':
    daily = True
    filename = 'bitcoin_daily.csv'
elif sys.argv[1] == 'weekly':
    weekly = True
    filename = 'bitcoin_weekly.csv'
else:
    print("Usage: python scaledata.py <hourly/daily/weekly>")
    exit(-1)

# The maximum for a timeframe for which we get daily data is 270.
# Therefore we could go back 269 days. However, since there might
# be issues when rescaling, e.g. zero entries, we should have an
# overlap that does not consist of only one period. Therefore,
# I limit the step size to 250. This leaves 19 periods for overlap.
if daily:
    maxstep=269
    overlap=40
    #step    = maxstep - overlap + 1
    dt = timedelta(days=maxstep)
    time_fmt = '%Y-%m-%d'
# Hourly time resolution needs a 7-day step
elif hourly:
    overlap = 18
    step    = 168
    dt = timedelta(hours=step)
    time_fmt = '%Y-%m-%dT%H'
elif weekly:
    overlap = 840
    maxstep = 1825
    dt = timedelta(days=maxstep)
    time_fmt = '%Y-%m-%d'
kw_list = ['Bitcoin']
start_date = datetime(2015, 1, 1).date()


## FIRST RUN ##
from pytrends.request import TrendReq as UTrendReq
GET_METHOD='get'

import requests

headers ={
 'authority': 'trends.google.com',
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'en-US,en;q=0.9',
    'content-type': 'application/json;charset=UTF-8',
    # Requests sorts cookies= alphabetically
    # 'cookie': '__utma=10102256.139027882.1665058480.1665058480.1665058480.1; __utmc=10102256; __utmz=10102256.1665058480.1.1.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided); __utmt=1; __utmb=10102256.38.9.1665060381408; HSID=AMz_jl8Iwb69A4n3S; SSID=AteFMU2GK_xzE1fcV; APISID=uG8y3aWNoX30fnnr/A1DmlMx4lrmkujuYG; SAPISID=Zfw5PJQZbZJ7EU0U/AxEFkPJi6YU5Tpjw4; __Secure-1PAPISID=Zfw5PJQZbZJ7EU0U/AxEFkPJi6YU5Tpjw4; __Secure-3PAPISID=Zfw5PJQZbZJ7EU0U/AxEFkPJi6YU5Tpjw4; SID=OQjtrXv3AN6nxCdtHBw4m8tnYNjEm7SIsKfjEaIrKam7pPI0YXejzLlok5ISK7H-tfz5tw.; __Secure-1PSID=OQjtrXv3AN6nxCdtHBw4m8tnYNjEm7SIsKfjEaIrKam7pPI0ec90qyfZf54Q82Upgjg1XQ.; __Secure-3PSID=OQjtrXv3AN6nxCdtHBw4m8tnYNjEm7SIsKfjEaIrKam7pPI0nHP9IWCD5_OfdQ3nJzIT5g.; AEC=AakniGMARFqHksDsE0w2xgzzqg2wp-Qf3eS4uJihwWc0cJBc2GQZn_liB1g; NID=511=SfCV1aE6cZ55dYDzrI71eLOZVihxy8GJTxV4Im1p7bkEPuxp1B4_tLGVUSnSaS8pmFhNzJ6TZqC1N5k4Tsb3eCFlhN-H9jyZd-yoiGBbtysrzhSKZe1KeYXQy0e-bWRwAgwl5yxq9S94XlTz7LIvUTXNMFg1WdigZou_S-bUZhbM3VijFqLP2JL3WiBDdk6KHd5wAnk5JEpHFEMOx-dhnPtXtUmRHhiQ_Ssha74Liu_0lxALM4wVmonTu8OtZgam2A-MsxfcaTIAprGPauWLvkVtrzq9YAhCDCRskA1mnWXaWrdL3mtMVZoc7hMFldjNYSHyyfIjWvkobX3eAGhYkfaIVimhEgwIfIKKPXdcc70ZgY4kFRy_Fok7; SEARCH_SAMESITE=CgQIx5YB; 1P_JAR=2022-10-06-12; SIDCC=AEf-XMRApLlCT4CWFDjpo4k1sZa8WYW-7Kw3AAx4tFh5Z6VcNkb5VtygAQoRUgrtWw3GB_BUv02f; __Secure-1PSIDCC=AEf-XMSrl6zV_h-lMopsP94U_yf8OlOKEEfMCgA7Z3oWTOks2ER4B4EcvMjibmKJFsjbO9046BM; __Secure-3PSIDCC=AEf-XMS2rDZzUPVxZgqNVNaj5WvQ2jEuCXnIPgfy139DvUFCcrGGmisqw-2UJni1Cx_Wc4js2R84',
    'origin': 'https://trends.google.com',
    'referer': 'https://trends.google.com/trends/explore?date=now%201-H&q=bitcoin',
    'sec-ch-ua': '"Google Chrome";v="105", "Not)A;Brand";v="8", "Chromium";v="105"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36',
    'x-client-data': 'CIa2yQEIpbbJAQjBtskBCKmdygEI2evKAQiSocsBCPW7zAEI/bzMAQiZxswBCOLLzAEIn9HMAQif38wBCLjfzAEI8d/MAQjE4cwBCMXhzAE=',
}


class TrendReq(UTrendReq):
    def _get_data(self, url, method=GET_METHOD, trim_chars=0, **kwargs):
        return super()._get_data(url, method=GET_METHOD, trim_chars=trim_chars, headers=headers, **kwargs)
# Login to Google. Only need to run this once, the rest of requests will use the same session.
pytrend = TrendReq()

# Run the first time (if we want to start from today, otherwise we need to ask for an end_date as well
today = datetime.today().date()
old_date = today

# Go back in time
new_date = today - dt #timedelta(hours=step)

# Create new timeframe for which we download data
timeframe = new_date.strftime(time_fmt)+' '+old_date.strftime(time_fmt)
print(timeframe)
pytrend.build_payload(kw_list=kw_list, timeframe = timeframe,geo='',gprop='')
interest_over_time_df = pytrend.interest_over_time()

## RUN ITERATIONS
# Note this runs backwards from the most recent date back.
while new_date>start_date:
    

    old_date = new_date + timedelta(hours=overlap-1)
    
    new_date = new_date - dt #timedelta(hours=step)
    # If we went past our start_date, use it instead
    if new_date < start_date:
        new_date = start_date
        
    # New timeframe
    timeframe = new_date.strftime(time_fmt)+' '+old_date.strftime(time_fmt)
    print(timeframe)

    # Download data
    pytrend.build_payload(kw_list=kw_list, timeframe = timeframe)
    temp_df = pytrend.interest_over_time()
    if (temp_df.empty):
        raise ValueError('Google sent back an empty dataframe. Possibly there were no searches at all during the this period! Set start_date to a later date.')
    # Renormalize the dataset and drop last line
    for kw in kw_list:
        beg = new_date
        end = old_date - timedelta(hours=1)
        
        # Since we might encounter zeros, we loop over the
        # overlap until we find a non-zero element
        for t in range(1,overlap+1):
            #print('t = ',t)
            #print(temp_df[kw].iloc[-t])
            if temp_df[kw].iloc[-t] != 0:
                # TODO dame da kore...
                
                scaling = float(interest_over_time_df[kw].iloc[t-1])/temp_df[kw].iloc[-t]
                #print('Found non-zero overlap!')
                print(scaling)
                break
            elif t == overlap:
                print('Did not find non-zero overlap, set scaling to zero! Increase Overlap!')
                scaling = 0
        # Apply scaling
        temp_df.loc[beg:end,kw]=temp_df.loc[beg:end,kw]*scaling
    interest_over_time_df = pd.concat([temp_df[:-overlap],interest_over_time_df])
    time.sleep(3)

# Save dataset
interest_over_time_df.to_csv(filename)
