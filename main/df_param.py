# -*- coding: utf-8 -*-
import json
import pandas as pd
from pandas import DataFrame
import csv
from csv import DictWriter
from csv import reader
import io
import time
import sys
import matplotlib.pyplot as plt
import numpy as np

def populate(data):
	data.index = pd.to_datetime(data.index, dayfirst=True)

	data['12d_EMA'] = data.price.ewm(span=12, adjust=False).mean()
	data['26d_EMA'] = data.price.ewm(span=26, adjust=False).mean()
	data['macd'] = data['12d_EMA']- data['26d_EMA']
	data['macdsignal'] = data.macd.ewm(span=9, adjust=False).mean()
	# returns = (closePrice@T)/(closePrice@(T-1)) - 1
	#data['returns'] = data.price.pct_change()
	data['returns'] = (data['price']/data['price'].shift(1)) - 1
	data['trading_signal'] = np.where(data['macd'] > data['macdsignal'], 1, -1)
	data['strategy_returns'] = data.returns * data.trading_signal.shift(1)
	data['MA50'] = data['price'].rolling(50).mean()
	# Total return on Day T from Day 1
	data['CUM'] = (1 + data['returns']).cumprod()
	data['cum_strategy_ret'] = (data.strategy_returns + 1).cumprod()
	# Compound Annual Growth Rate
	# Total number of trading days
	days = len(data['cum_strategy_ret'])
	# 252 = total trading days in a year
	data['annual_ret'] = (data['cum_strategy_ret'].iloc[-1]**(252/days) - 1)*100
	# Calculate the annualised volatility the variation in stcok priice over a time period
	data['annual_volatility'] = data['strategy_returns'].std() * np.sqrt(252) * 100
	# Sharpe ratio : the risk taken in comparision to risk free investments(FD/RD/Bank Savings)
	# Assume the annual risk-free rate is 4%, as bank return principal at 4% interest
	# 252 = total trading days in a year
	risk_free_rate = 0.04
	data['daily_risk_free_return'] = risk_free_rate/252
	# Calculate the excess returns by subtracting the daily returns by daily risk-free return
	data['excess_daily_returns'] = data['strategy_returns'] - data['daily_risk_free_return']
	# Calculate the sharpe ratio using the given formula
	sharpe_ratio = (data['excess_daily_returns'].mean() /
        	        data['excess_daily_returns'].std()) * np.sqrt(252)
	#print('The Sharpe ratio is %.2f' % sharpe_ratio)

def read_file(fl):
    df = pd.read_csv(fl)
    return df

def get_df(symbol):
    base_path = 'price_list/'
    fl_name = base_path + symbol + '.csv'
    df = read_file(fl_name)
    df['price']=df['Close']
    populate(df)
    new=pd.DataFrame()
    new['price']=df['price']
    new['Close']=df['Close']
    return new['price']
