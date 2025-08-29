# -*- coding: utf-8 -*-
"""
Created on Tue Apr 15 19:48:27 2025

@author: julia
data loading, cleaning, merging, CPR calculation, plots, merged dataframe
"""

import pandas as pd
import pandas_datareader as pdr
import numpy as np
import numpy_financial as npf
import matplotlib.pyplot as plt
import seaborn as sns
#load data

fm_df = pd.read_csv(r"C:\Users\julia\OneDrive\Desktop\Practicum\MBS_Pool_Details.csv", low_memory=False)
yields = pd.read_csv(r"C:\Users\julia\OneDrive\Desktop\Practicum\cusipsandYieldscsv.csv", low_memory=False)

# make sure column names are lower case
fm_df.columns = fm_df.columns.str.lower()
yields.columns = yields.columns.str.lower()

#cleanup whitespace
fm_df['cusip_id'] = fm_df['cusip_id'].str.strip()
yields['cusip_id'] = yields['cusip_id'].str.strip()

#capitalization
fm_df['cusip_id'] = fm_df['cusip_id'].str.upper()
yields['cusip_id'] = yields['cusip_id'].str.upper()

#check for strings datatype
fm_df['cusip_id'] = fm_df['cusip_id'].astype(str)
yields['cusip_id'] = yields['cusip_id'].astype(str)

#merge on cusip_id
merged = pd.merge(fm_df, yields, on = 'cusip_id', how = 'inner', indicator = True)

#summary of merged results
print(merged['_merge'].value_counts())


#%%

#calculate principal payments
merged['principal_paid_off'] = merged["issuance upb"] - merged["current upb"]

#calculate monthly interest rate
merged['monthly_interest_rate'] = merged['wa interest rate']/100/12

merged = merged.dropna(subset = ['wa loan age', 'wa orig term', 'monthly_interest_rate', 'issuance upb'])


def scheduled_principal_paid(row):
    months = np.arange(1, int(row['wa loan age']) + 1)
    
    principal_pmts = npf.ppmt(
        rate = row['monthly_interest_rate'],
        nper = row['wa orig term'],
        per = months,
        pv = -row['issuance upb'])
    
    scheduled_principal_paid = principal_pmts.sum()
    return scheduled_principal_paid

merged['scheduled principal paid'] = merged.apply(scheduled_principal_paid, axis = 1)

#%% calculating CPR

merged['scheduled_balance'] = merged['issuance upb'] - merged['scheduled principal paid']

merged['prepayment'] = merged['scheduled_balance'] - merged['current upb']

merged['SMM'] = 1 - (merged['current upb'] / merged['scheduled_balance'])**(1/merged['wa loan age'])

merged['calculated_CPR'] = (1 - (1-merged['SMM'])**12) *100

#%% compare calculated CPR to CPR found on Bloomberg terminal
new_df = merged[['cusip_id', 'calculated_CPR','cpr_y', 'yields']]

#%% create bins on related FICO scores

bins_FICO = [300, 620, 660, 700, 740,800, 850]
FICO_labels = ['<620', '620-659', '660-699', '700-739', '740-799', '800+']
merged['FICO Group'] = pd.cut(merged['wa credit score'], bins = bins_FICO, 
                          labels = FICO_labels, right= False)

#now group by FICO score and calculate average CPR 
grouped = merged.groupby('FICO Group')['cpr_y'].mean()
print(grouped)

# plot calculated CPR against FICO score


plt.figure(figsize = (10,6))
grouped.plot(kind = 'bar', color = 'green')
plt.title("Average Benchmark CPR Against Grouped FICO Scores")
plt.xlabel("FICO Score Group")
plt.ylabel("Average Benchmark CPR (%)")
plt.grid(True)
plt.show()

#%% 
#calculate average CPR across all loan pools

average_CPR = merged['calculated_CPR'].mean()
print(f'Mean CPR across all pools: {average_CPR}')

cpr_sigma = merged['CPR'].stdev()

#%%
#def calculatePrepayment(issuance_upb, scheduled_balance, interest_rate):
    
#%% plot yields against calculated and benchmark CPR

sns.set(style = 'whitegrid', font_scale = 1.2)

plt.figure(figsize = (10,6))
sns.scatterplot(data = new_df, y = 'yields', x = 'calculated_CPR', label = 'Calculated CPR', color = 'blue')

sns.scatterplot(data = new_df, y= 'yields', x='cpr_y', label = 'Bloomberg Benchmark CPR', color = 'black')

plt.ylabel('Yield (%)')
plt.xlabel('CPR (%)')
plt.title('Calculated CPR and Benchmark CPR vs. Yield')
plt.legend()
plt.tight_layout()
plt.show()

#%% find interest rates to compare against prepayment and plot

interest_rates = pdr.DataReader("rate", "fred", start = '2024-04-01')

plt.figure(figsize = (10,6))
sns.scatterplot(data = interest_rates,)



