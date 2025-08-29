# -*- coding: utf-8 -*-
"""
Created on Sun May  4 18:37:56 2025

@author: julia
"""

import pandas as pd
import matplotlib.pyplot as plt

LUMSTRUUM = pd.read_excel(r"C:\Users\julia\OneDrive\Desktop\Practicum\LUMSTRUU_MONTHLYDATA.xlsx", skiprows=5)
MortgageRate = pd.read_excel(r"C:\Users\julia\OneDrive\Desktop\Practicum\30ymortgagedata_monthly.xlsx", skiprows = 5)
Treasury = pd.read_excel(r"C:\Users\julia\OneDrive\Desktop\Practicum\10yrtreasury_monthlydata.xlsx", skiprows = 5)
MidInterestRates = pd.read_excel(r"C:\Users\julia\OneDrive\Desktop\Practicum\fdtrmid_monthly.xlsx", skiprows = 5)
#%%
for df in [LUMSTRUUM, MortgageRate, Treasury,MidInterestRates]:
    df['Date'] = pd.to_datetime(df['Date'])
    df.set_index('Date', inplace = True)
    
#merge all dfs on Date
dfs = [LUMSTRUUM, MortgageRate, Treasury, MidInterestRates]
merged = pd.concat(dfs, axis =1, join = 'inner')
print(merged.isna().sum())
merged.columns = ['PX_LAST_LUMSTRUUM', 'CHG_PCT_1D_LUMSTRUUM',
                  'PX_LAST_MortgageRate', 'CHG_PCT_1D_MortgageRate',
                  'PX_LAST_Treasury', 'CHG_PCT_1D_Treasury',
                  'PX_LAST_MidInterestRates', 'CHG_PCT_1D_MidInterestRates']
#%%
print(merged.columns)
print(merged.head())
print(merged[['PX_LAST_LUMSTRUUM', 'PX_LAST_MortgageRate', 'PX_LAST_Treasury', 'PX_LAST_MidInterestRates']].describe())
print(merged.isna().sum())
#%%
fig, ax1 = plt.subplots(figsize = (12,6))

ax1.plot(merged.index, merged['PX_LAST_LUMSTRUUM'], label = 'MBS Index (LUMSTRUUM)', color = 'tab:blue')
ax1.set_ylabel('MBS Index (LUMSTRUUM)', color = 'tab:blue')
ax1.tick_params(axis = 'y', labelcolor = 'tab:blue')

#secondary y-axis for rates
ax2 = ax1.twinx()
ax2.plot(merged.index, merged['PX_LAST_MortgageRate'], label = '30Y Mortgage Rate', color = 'tab:orange')
ax2.plot(merged.index, merged['PX_LAST_Treasury'], label = '10Y Treasury Rate', color = 'tab:green')
ax2.plot(merged.index, merged['PX_LAST_MidInterestRates'], label = 'Mid Fed Funds Rate', color = "tab:red")
ax2.set_ylabel('Interest Rate (%)', color = 'tab:red')
ax2.tick_params(axis = 'y', labelcolor = 'tab:red')
            
#add legends
lines_1, labels_1 = ax1.get_legend_handles_labels()
lines_2, labels_2 = ax2.get_legend_handles_labels()
ax2.legend(lines_1 + lines_2, labels_1 + labels_2, loc = 'upper left')


plt.title("Rates and MBS Index over time")
plt.xlabel("Date")
plt.ylabel("Value")
plt.legend()
plt.tight_layout()
plt.show()




