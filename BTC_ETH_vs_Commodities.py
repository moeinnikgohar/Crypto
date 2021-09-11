#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy
import pandas
import matplotlib
import math
import random
import statsmodels


# In[2]:


import pandas_datareader #don't forget to pip install it in the terminal (pip install pandas_datareader)
import numpy as np
import pandas as pd
from pandas_datareader import data as wb


# In[3]:


from yahoofinancials import YahooFinancials
import pickle
import quandl
from datetime import datetime


# In[4]:


import plotly.offline as py #pip install plotly in terminal
import plotly.graph_objs as go
import plotly.figure_factory as ff
py.init_notebook_mode(connected=True)


# In[5]:


#################Q1: Retrieve and plot the Bitcoin, Ethereum prices for the last 2 years#######################


# In[6]:


def get_quandl_data(quandl_id):
    '''Download and cache Quandl dataseries'''
    cache_path = '{}.pkl'.format(quandl_id).replace('/','-')
    try:
        f = open(cache_path, 'rb')
        df = pickle.load(f)   
        print('Loaded {} from cache'.format(quandl_id))
    except (OSError, IOError) as e:
        print('Downloading {} from Quandl'.format(quandl_id))
        df = quandl.get(quandl_id, returns="pandas")
        df.to_pickle(cache_path)
        print('Cached {} at {}'.format(quandl_id, cache_path))
    return df


# In[7]:


# Pull Kraken BTC price exchange data
btc_usd_price_kraken = get_quandl_data('BCHARTS/KRAKENUSD')


# In[8]:


btc_usd_price_kraken.head()


# In[9]:


BTC = quandl.get("BCHARTS/KRAKENUSD")


# In[10]:


BTC.tail(730)


# In[11]:


# Chart the BTC pricing data
btc_trace = go.Scatter(x=btc_usd_price_kraken.tail(755).index, y=btc_usd_price_kraken['Weighted Price'])
py.iplot([btc_trace])


# In[12]:


# Pull Bitfinex ETH price exchange data
eth_usd_price_bitfinex = get_quandl_data('BITFINEX/ETHUSD')


# In[13]:


eth_usd_price_bitfinex.head()


# In[14]:


ETH = quandl.get("BITFINEX/ETHUSD")


# In[15]:


ETH.tail(730)


# In[16]:


# Chart the ETH pricing data
eth_trace = go.Scatter(x=eth_usd_price_bitfinex.tail(755).index, y=eth_usd_price_bitfinex['Bid'])
py.iplot([eth_trace])


# In[17]:


#################Q2: Plot the Ethereum to GBP price for the last year#######################


# In[18]:


# Pull Bitfinex ETH price exchange data
eth_gbp_price_bitfinex = get_quandl_data('BITFINEX/ETHGBP')


# In[19]:


eth_gbp_price_bitfinex.tail(365)


# In[20]:


# Chart the ETH pricing data
eth_trace = go.Scatter(x=eth_gbp_price_bitfinex.tail(365).index, y=eth_gbp_price_bitfinex['Bid'])
py.iplot([eth_trace])


# In[21]:


#################Q3: Retrieve and plot the Gas price in GBP for the last year###################


# In[22]:


UKOG=wb.DataReader('UKOG.L', data_source='yahoo', start='2018-7-26')


# In[23]:


UKOG


# In[24]:


# Chart the UKOG pricing data
UKOG_trace = go.Scatter(x=UKOG.index, y=UKOG['Adj Close'])
py.iplot([UKOG_trace])


# In[25]:


#################Q4: Resample the data to obtain Ethereum and Gas prices on a monthly and weekly basis###################


# In[26]:


#W: weekly frequency, M: month end frequency, SM: semi-month end frequency (15th & end of month), Q: quarter end frequency


# In[27]:


UKOG_monthly_resampled_data = UKOG.Close.resample('M').mean()


# In[28]:


UKOG_monthly_resampled_data


# In[29]:


UKOG_weekly_resampled_data = UKOG.Close.resample('W').mean()


# In[30]:


UKOG_weekly_resampled_data


# In[31]:


ETH_monthly_resampled_data = eth_gbp_price_bitfinex.Bid.resample('M').mean()


# In[32]:


ETH_monthly_resampled_data


# In[33]:


ETH_weekly_resampled_data = eth_gbp_price_bitfinex.Bid.resample('W').mean()


# In[34]:


ETH_weekly_resampled_data


# In[35]:


#######Q5. Calculate the correlation between Ethereum and Gas price in the last year using the weekly dataset / #########
###########do you notice anything?#########


# In[36]:


#The weekly resampled data for UKOG and ETH will be merged together into a single excel file before correlation analysis
#the merged excel file will be submitted with the script


# In[37]:


from scipy import stats


# In[38]:


ETH_weekly_resampled_data.to_excel('Desktop/Python/ETH_weekly.xlsx')


# In[39]:


UKOG_weekly_resampled_data.to_excel('Desktop/Python/UKOG_weekly.xlsx')


# In[40]:


ETH_UKOG_weekly=pd.read_excel('Desktop/Python/ETH_UKOG_weekly.xlsx')


# In[ ]:


ETH_UKOG_weekly['ETH'].corr(ETH_UKOG_weekly['UKOG'])


# In[ ]:


#Value of 0.43 indicates a moderate positive linear relationship between ETH and UKOG price
#This means that Gas price and ETH price is moderately dependent 


# In[ ]:


#######Q6. Calculate the relative movement of Ethereum’s with respect to Bitcoin. Do you notice anything?#########


# In[ ]:


#ETH data will be merged withBTC data and the correlation between them will be measured


# In[ ]:


ETH = get_quandl_data('BITFINEX/ETHUSD')


# In[ ]:


ETH.tail(730).to_excel('Desktop/Python/ETH.xlsx')


# In[ ]:


BTC.tail(730).to_excel('Desktop/Python/BTC.xlsx')


# In[ ]:


BTC_ETH_2_years=pd.read_excel('Desktop/Python/BTC_ETH_2_years.xlsx')


# In[ ]:


BTC_ETH_2_years['BTC'].corr(BTC_ETH_2_years['ETH'])


# In[ ]:


#Value of 0.45 indicates a moderate positive linear relationship between BTC and ETH price
#This means that BTC price and ETH price is moderately dependent. ETH price is slightly more dependent on BTC than UKOG


# In[ ]:


#######Q7. Based on what you calculated in VI. what can you expect from the beta factor between Ethereum and bitcoin? 
###############Bonus: calculate the beta factor for these two assets. #########


# In[ ]:


BTC_ETH_2_years['ETH'].cov(BTC_ETH_2_years['BTC'])


# In[ ]:


BTC_ETH_2_years['BTC'].var()


# In[ ]:


Beta= (BTC_ETH_2_years['ETH'].cov(BTC_ETH_2_years['BTC']))/(BTC_ETH_2_years['BTC'].var())


# In[ ]:


Beta


# In[ ]:


#the beta value is very close to zero. this indicates a zero systematic risk.
#this means that that BTC would have the same expected return as ETH
#so this means the price of BTC does not fluctuate as a result of ETH


# In[ ]:


####Below is an alternative way of recording live results of BTC and ETH####


# In[ ]:


import requests
import json


# In[ ]:


response = requests.get('https://api.coinbase.com/v2/prices/BTC-USD/spot')
data = json.dumps(response.json())
print (data)


# In[ ]:


response = requests.get('https://api.coinbase.com/v2/prices/ETH-USD/spot')
data = json.dumps(response.json())
print (data)

