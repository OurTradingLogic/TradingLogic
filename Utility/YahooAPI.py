import yfinance as yf
from yahoo_fin import stock_info as si
import pandas as pd 
import numpy as np
from datetime import datetime, timedelta
import Utility.Constant as cons
from collections import defaultdict

class YahooAPI:  
    def __init__(self, stocklist) -> None:
        super().__init__()
        self.__auto_adjust = False
        self.__progress_bar = True
        self.__stocksData = defaultdict(list)
        self.__ticketList = self.__amdentMarketSuffix(stocklist)
        self.__tickets = yf.Tickers(self.__ticketList)

    def __amdentMarketSuffix(self, stocklist):
        tickersresult = []
        for stock in stocklist:
            tickersresult.append(stock['tradingsymbol'] + ".NS") 

        return tickersresult  

    def __constructData(self, stocksData):
        for index, stock in stocksData.iterrows():  
            openList = []   
            highList = []  
            lowList = []  
            closeList = []  
                          
            for stockname, openprice in stock['Open'].iteritems():
                openList.append({"StockName": stockname, "OpenPrice":openprice})

            for stockname, highprice in stock['High'].iteritems():
                highList.append({"StockName": stockname, "HighPrice":highprice})

            for stockname, lowprice in stock['Low'].iteritems():
                lowList.append({"StockName": stockname, "LowPrice":lowprice})

            for stockname, closeprice in stock['Close'].iteritems():
                closeList.append({"StockName": stockname, "ClosePrice":closeprice})

            i = 0
            list_cnt = len(openList)
            while i < list_cnt:
                if np.isnan(openList[i]["OpenPrice"]):
                    i += 1
                    continue
                data = {"date":index,"open":openList[i]["OpenPrice"],"high":highList[i]["HighPrice"],"low":lowList[i]["LowPrice"],"close":closeList[i]["ClosePrice"]}
                self.__stocksData[openList[i]["StockName"]].append(data)
                i += 1
        self.__fillNAN()

    def __fillNAN(self):     
        for stockData in self.__stocksData.values():
            prevCloseValue=np.nan
            prevHighValue=np.nan
            prevLowValue=np.nan
            prevOpenValue=np.nan 
            haveNANValue = [item for item in stockData if np.isnan(item["close"])\
                or np.isnan(item["high"]) or np.isnan(item["low"])\
                or np.isnan(item["open"])] 
            if len(haveNANValue) == 0:
                continue
            for data in reversed(stockData):
                closeprice = data["close"]
                if np.isnan(closeprice) and (prevCloseValue != np.nan or np.isnan(prevCloseValue)): 
                    data['close'] = prevCloseValue
                if closeprice!= np.nan or not np.isnan(closeprice):
                    prevCloseValue = closeprice

                highprice = data["high"]
                if np.isnan(highprice) and (prevHighValue != np.nan or np.isnan(prevHighValue)): 
                    data['high'] = prevHighValue
                if highprice!= np.nan or not np.isnan(highprice):
                    prevHighValue = highprice

                lowprice = data["low"]
                if np.isnan(lowprice) and (prevLowValue != np.nan or np.isnan(prevLowValue)): 
                    data['low'] = prevLowValue
                if lowprice!= np.nan or not np.isnan(lowprice):
                    prevLowValue = lowprice

                openprice = data["open"]
                if np.isnan(openprice) and (prevOpenValue != np.nan or np.isnan(prevOpenValue)): 
                    data['open'] = prevOpenValue
                if openprice!= np.nan or not np.isnan(openprice):
                    prevOpenValue = openprice
    
    def GetResult(self):
        #result = pd.DataFrame.from_dict(self.__stocksData)
        return self.__stocksData

    def GetStockResult(self, stockname):
       return self.__stocksData[stockname] 

    def history_period(self, period):
        data = self.__tickets.history(period)
        self.__constructData(data)
        return self

    def __constructSingleStockData(self, data, stockName):      
        for index, row in data.iterrows():
            data = {"date":index,"open":row['Open'],"high":row['High'],"low":row['Low'],"close":row['Close']}
            self.__stocksData[stockName].append(data)
        
        self.__fillNAN()

    def history_data(self, start, end, interval):
        if len(self.__ticketList) == 1:
            data = yf.download(tickers=self.__ticketList, start=start, end=end, interval=interval, \
                auto_adjust=self.__auto_adjust, progress=self.__progress_bar)  
            self.__constructSingleStockData(data, self.__ticketList[0])         
        else:
            data = self.__tickets.download(start=start, end=end, interval=interval, \
                auto_adjust=self.__auto_adjust, progress=self.__progress_bar)  
            self.__constructData(data)
        
        return self

def amdentNS(tickers):
    tickersresult = []
    for ticket in tickers:
        tickersresult.append(ticket['tradingsymbol'] + ".NS") 

    return tickersresult   

def get_historic_data2(tickers, start, end, interval):
    if len(tickers) > 1:
       tickers_result = amdentNS(tickers) 
    elif tickers[0] != '^':
        tickers_result = tickers + '.NS'

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