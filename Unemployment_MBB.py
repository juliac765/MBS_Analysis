# -*- coding: utf-8 -*-
"""
Created on Sat Apr 12 09:52:40 2025

@author: julia
"""

import pandas_datareader as pdr
from darts import TimeSeries
import yfinance as yf
import matplotlib.pyplot as plt

#%% load unemployment rate into pandas dataframe
ir_df = pdr.DataReader("GS10", "fred", start = '2008-01-01').dropna()
ir_df = ir_df.resample('ME').last() #resamples to monthly data 

series = TimeSeries.from_dataframe(ir_df, value_cols = "GS10", fill_missing_dates=False, freq='M')

#%% 10-year treasury yield
#treasury_yield_df = pdr.DataReader("DGS10", "fred", start = '2008-01-01').dropna()
#treasury_yield_df = treasury_yield_df.resample('ME').last()

#%% consumer price index
cpi_df = pdr.DataReader("CPIAUCSL", 'fred', start = '2008-01-01').dropna()
cpi_df = cpi_df.resample('ME').last()
#%% use yahoo finance to download data for MBB
MBB_df = yf.download("MBB", start = '2008-01-01').dropna()
MBB_df = MBB_df['Close'].resample('ME').last()

#%% create a timeseries with darts
series = TimeSeries.from_dataframe(MBB_df, value_cols= "MBB", fill_missing_dates=False, freq = 'M')
#%% 3. plot the data
plt.figure(figsize = (12,6))

plt.plot(ir_df.index, ir_df['GS10'], label = '10 year treasury yield', color = 'Red')
plt.plot(MBB_df.index, MBB_df, color = 'blue', label="MBB price")
plt.plot(cpi_df.index, cpi_df, color = 'green', label = 'CPI Index')
plt.title("10-year Treasury vs MBB")
plt.xlabel('Date')
plt.ylabel("MBB Price")
plt.legend()
plt.show()
#%%
#10-year treasury yield
#plt.plot(treasury_yield_df.index,treasury_yield_df['DGS10'], label ="10-year treasury yield",
           #color = 'green')

#cpi
#plt.plot(cpi_df.index, cpi_df['CPIAUCSL'], label = 'CPI', color = 'red')

#MBB ETF price
plt.plot(MBB_df.index, MBB_df, 
           label = 'MBB ETF Price Over Time', color = 'purple')

plt.title('Economic indicators and MBB ETF Price Over time')
plt.xlabel('Date')
plt.ylabel('Value')
plt.grid()
plt.legend()




plt.tight_layout()
plt.show()
