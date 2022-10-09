import yfinance as yf
from yahoo_fin import stock_info as si
import pandas as pd 
import numpy as np
from datetime import datetime, timedelta
import Utility.Constant as cons

def amdentNS(tickers):
    tickersresult = []
    for ticket in tickers:
        tickersresult.append(ticket['tradingsymbol'] + ".NS") 

    return tickersresult   

def get_historic_data2(tickers, start, end, interval):
    tickers_result = amdentNS(tickers)

    data = yf.download(tickers=tickers_result, start=start, end=end, interval=interval)
  
    date = []
    open = []
    high = []
    low = []
    close = []
    prevopen = []
    prevhigh = []
    prevlow = []
    prevclose = []
    
    for index, row in data.iterrows():
        date.append(index)
        open.append(row['Open'])
        high.append(row['High'])
        low.append(row['Low'])
        close.append(row['Close'])
    
    date_df = pd.DataFrame(date).rename(columns = {0:'date'})
    open_df = pd.DataFrame(open).rename(columns = {0:'open'})
    high_df = pd.DataFrame(high).rename(columns = {0:'high'})
    low_df = pd.DataFrame(low).rename(columns = {0:'low'})
    close_df = pd.DataFrame(close).rename(columns = {0:'close'})
    frames = [date_df, open_df, high_df, low_df, close_df]
    df = pd.concat(frames, axis = 1, join = 'inner')
    return df

def get_historic_data(tickers, start, end, interval):
    if tickers[0] != '^':
        tickers = tickers + '.NS'
    data = yf.download(tickers=tickers, start=start, end=end, interval=interval)
  
    date = []
    open = []
    high = []
    low = []
    close = []
    prevopen = []
    prevhigh = []
    prevlow = []
    prevclose = []
    
    for index, row in data.iterrows():
        date.append(index)
        open.append(row['Open'])
        high.append(row['High'])
        low.append(row['Low'])
        if np.isnan(row['Close']) and (len(close) > 0): 
            close.append(close[len(close)-1])
        else:
            close.append(row['Close'])
    
    date_df = pd.DataFrame(date).rename(columns = {0:'date'})
    open_df = pd.DataFrame(open).rename(columns = {0:'open'})
    high_df = pd.DataFrame(high).rename(columns = {0:'high'})
    low_df = pd.DataFrame(low).rename(columns = {0:'low'})
    close_df = pd.DataFrame(close).rename(columns = {0:'close'})
    frames = [date_df, open_df, high_df, low_df, close_df]
    df = pd.concat(frames, axis = 1, join = 'inner')
    return df

def get_last_day_data(tickers):
    if tickers[0] != '^':
      tickers = tickers + '.NS'
    data = yf.download(tickers, period="1d", interval="1d", rounding=True)
    date = []
    open = []
    high = []
    low = []
    close = []
    
    for index, row in data.iterrows():
        date.append(index)
        open.append(row['Open'])
        high.append(row['High'])
        low.append(row['Low'])
        if np.isnan(row['Close']) and (len(close) > 0): 
            close.append(close[len(close)-1])
        else:
            close.append(row['Close'])
    
    date_df = pd.DataFrame(date).rename(columns = {0:'date'})
    open_df = pd.DataFrame(open).rename(columns = {0:'open'})
    high_df = pd.DataFrame(high).rename(columns = {0:'high'})
    low_df = pd.DataFrame(low).rename(columns = {0:'low'})
    close_df = pd.DataFrame(close).rename(columns = {0:'close'})
    frames = [date_df, open_df, high_df, low_df, close_df]
    df = pd.concat(frames, axis = 1, join = 'inner')
    return df

def get_one_day_data(tickers, start, interval):
    if tickers[0] != '^':
      tickers = tickers + '.NS'

    enddate1 = start + timedelta(days=0, minutes=cons.MARKET_TOTAL_MIN)
    data = yf.download(tickers=tickers, start=start, end=enddate1, interval=interval, rounding=True)
    date = []
    open = []
    high = []
    low = []
    close = []
    
    for index, row in data.iterrows():
        date.append(index)
        open.append(row['Open'])
        high.append(row['High'])
        low.append(row['Low'])
        if np.isnan(row['Close']) and (len(close) > 0): 
            close.append(close[len(close)-1])
        else:
            close.append(row['Close'])
    
    date_df = pd.DataFrame(date).rename(columns = {0:'date'})
    open_df = pd.DataFrame(open).rename(columns = {0:'open'})
    high_df = pd.DataFrame(high).rename(columns = {0:'high'})
    low_df = pd.DataFrame(low).rename(columns = {0:'low'})
    close_df = pd.DataFrame(close).rename(columns = {0:'close'})
    frames = [date_df, open_df, high_df, low_df, close_df]
    df = pd.concat(frames, axis = 1, join = 'inner')
    return df

def get_live_price(tickers):
    if tickers[0] != '^':
      tickers = tickers + '.NS'
    return si.get_live_price(tickers)

def get_one_day_data_skip_holiday(tickers, index):
    if index.weekday() == 0:  
        startdate = index - timedelta(days=3)
    else:                    
        startdate = index - timedelta(days=1)

    stock = get_one_day_valid_data(tickers, start = startdate)
    
    return stock

def get_one_day_valid_data(tickers, start):
    stock = get_one_day_data(tickers, start, interval="1d")
                    
    #holiday finding
    while not len(stock) > 0:                   
        start = start - timedelta(days=1)
        stock = get_one_day_data(tickers, start, interval="1d")
    
    return stock