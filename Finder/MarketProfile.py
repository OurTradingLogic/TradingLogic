import pandas as pd
import numpy as np
import yfinance as yf
from datetime import datetime
import Enum.CommonEnum as enum
from collections import defaultdict
import Model.FinderModel as fmodel

class MarketProfile:
    _marketProfileResult = defaultdict(list)
    _stocksData = defaultdict(list)

    def __init__(self, stockData):
        self._stocksData = stockData 

    def findMarketProfile(self, freq='d'):
        marketProfileList = defaultdict()
        i = 0
        for stockname, data in self._stocksData.items():
            i = i + 1
            df = pd.DataFrame.from_dict(data)              
            if df['close'].isnull().all():
                continue

            #marketProfileList[stockname] = self.__market_profile(df)
            marketProfileList[stockname] = self.__market_profile(stockname, df, frequency= freq)

            if i == 1:
                break

        return marketProfileList
    
    def findMarketVolumnProfile(self, freq='d'):
        marketProfileList = defaultdict()
        i = 0
        for stockname, data in self._stocksData.items():
            i = i + 1
            df = pd.DataFrame.from_dict(data)              
            if df['close'].isnull().all():
                continue

            marketProfileList[stockname] = self.__volume_profile(df)

            if i == 1:
                break

        return marketProfileList

    #market_df should be in dataframe
    # df = pd.DataFrame.from_dict(data)              
    # if df['close'].isnull().all(): continue
    def __market_profile(self, market_df, height_precision = 1, frequency='d'):
        marketProfileResult = defaultdict(list)
        fin_prod_data = market_df.copy()
        fin_prod_data[('high')] = fin_prod_data[('high')] * height_precision
        fin_prod_data[('low')] = fin_prod_data[('low')] * height_precision
        fin_prod_data = fin_prod_data.round({'low': 0, 'high': 0})  

        time_groups = fin_prod_data.set_index('date')
        time_groups = time_groups.groupby(pd.Grouper(freq=frequency))['adjclose'].mean()
        #time_groups = time_groups.dropna()
        #time_groups = time_groups.reset_index(drop=True)

        current_time_group_index=0
        char_mark = 64

        # add max price as it will be ignored in for range loop above
        frequencyKey = str(time_groups.index[current_time_group_index])[5:7] + '/' + str(time_groups.index[current_time_group_index])[8:10]

        # build dictionary with all needed prices
        tot_min_price=min(np.array(fin_prod_data['low']))
        tot_max_price=max(np.array(fin_prod_data['high']))
        tot_range = int(tot_max_price) - int(tot_min_price)
        for r in range(0, tot_range):
            marketProfileResult[frequencyKey].append('')

        for x in range(0, len(fin_prod_data)):
            if fin_prod_data.iloc[x]['date'].date() > time_groups.index[current_time_group_index].date():
                # new time period
                char_mark=64
                current_time_group_index += 1              
                frequencyKey = str(time_groups.index[current_time_group_index])[5:7] + '/' + str(time_groups.index[current_time_group_index])[8:10]
                for i in range(0, tot_range):
                    marketProfileResult[frequencyKey].append('')

            char_mark += 1
            min_price=fin_prod_data.iloc[x]['low']
            max_price=fin_prod_data.iloc[x]['high']
            min_range = abs(min_price - tot_min_price)
            max_range = min_range + abs(max_price - min_price)
            for price in range(int(min_range), int(max_range)):
                tempValue = marketProfileResult[frequencyKey][price-1]
                tempValue+=(chr(char_mark))
                marketProfileResult[frequencyKey][price-1] = tempValue

        return fmodel.MarketProfileModel(tot_max_price, tot_min_price, marketProfileResult)

    #market_df should be in dataframe
    # df = pd.DataFrame.from_dict(data)              
    # if df['close'].isnull().all(): continue
    def __market_profile2(self, stockName, market_df, height_precision = 1, frequency='d'):
        marketProfileResult = defaultdict(list)
        fin_prod_data = market_df.copy()
        fin_prod_data[('high')] = fin_prod_data[('high')] * height_precision
        fin_prod_data[('low')] = fin_prod_data[('low')] * height_precision
        fin_prod_data = fin_prod_data.round({'low': 0, 'high': 0})  

        time_groups = fin_prod_data.set_index('date')
        time_groups = time_groups.groupby(pd.Grouper(freq=frequency))['adjclose'].mean()
        #time_groups = time_groups.dropna()
        #time_groups = time_groups.reset_index(drop=True)

        current_time_group_index=0
        mp = defaultdict(str)
        char_mark = 64

        # build dictionary with all needed prices
        tot_min_price=min(np.array(fin_prod_data['low']))
        tot_max_price=max(np.array(fin_prod_data['high']))
        for price in range(int(tot_min_price), int(tot_max_price)):
            mp[price]+=('\t')

        # add max price as it will be ignored in for range loop above
        mp[tot_max_price] = '\t' + str(time_groups.index[current_time_group_index])[5:7] + '/' + str(time_groups.index[current_time_group_index])[8:10]

        for x in range(0, len(fin_prod_data)):
            if fin_prod_data.iloc[x]['date'].date() > time_groups.index[current_time_group_index].date():
                # new time period
                char_mark=64
                # buffer and tab all entries
                buffer_max = max([len(v) for k,v in mp.items()])
                current_time_group_index += 1
                for k,v in mp.items():
                    mp[k] += (chr(32) * (buffer_max - len(mp[k]))) + '\t'
                mp[tot_max_price] += str(time_groups.index[current_time_group_index])[5:7] + '/' + str(time_groups.index[current_time_group_index])[8:10]


            char_mark += 1
            min_price=fin_prod_data.iloc[x]['low']
            max_price=fin_prod_data.iloc[x]['high']
            for price in range(int(min_price), int(max_price)):
                mp[price]+=(chr(char_mark))
    
        sorted_keys = sorted(mp.keys(), reverse=True)
        for x in sorted_keys:
            # buffer each list
            print(str("{0:.2f}".format((x * 1.0) / height_precision)) + ': \t' + ''.join(mp[x]))
            result = str("{0:.2f}".format((x * 1.0) / height_precision)) + ': \t' + ''.join(mp[x])
            marketProfileResult[stockName].append(result)

        return marketProfileResult

    def __volume_profile(self, market_df, height_precision = 1, frequency='d'):        
        df = market_df.copy()

        start_price = df['adjclose'].min()
        stop_price = df['adjclose'].max()
        from_date = df['date'].min()
        to_date = df['date'].max()

        low = start_price
        # delta means granularity in volume aggregation range, it is delta in price
        # the volume corresponds to price
        delta = (stop_price - start_price)/100    # here we are splitting whole price range into blocks
        high = 0

        vol_profile_list = []
        while high < stop_price:
            volume = 0    
            high = low + delta
            
            sub_df = df.loc[df['adjclose'].between(low, high, inclusive=False)]

            for i in sub_df.index.values:
                volume = volume + df.iloc[i]['volume']

            vol_profile = fmodel.MarketVolumnProfileModel(low, volume)
            vol_profile_list.append(vol_profile)
            low = high

        return fmodel.MarketVolumnProfileListModel(vol_profile_list, from_date, to_date)

#market_df should be in dataframe
# df = pd.DataFrame.from_dict(data)              
# if df['close'].isnull().all(): continue
def market_profile2(stockName, market_df, height_precision = 1, frequency='15min'):
    marketProfileResult = defaultdict(list)
    fin_prod_data = market_df.copy()
    fin_prod_data[('high')] = fin_prod_data[('high')] * height_precision
    fin_prod_data[('low')] = fin_prod_data[('low')] * height_precision
    fin_prod_data = fin_prod_data.round({'low': 0, 'high': 0})  

    time_groups = fin_prod_data.set_index('date')
    time_groups = time_groups.groupby(pd.Grouper(freq=frequency))['adjclose'].mean()

    current_time_group_index=0
    mp = defaultdict(str)
    char_mark = 64

    # build dictionary with all needed prices
    tot_min_price=min(np.array(fin_prod_data['low']))
    tot_max_price=max(np.array(fin_prod_data['high']))
    for price in range(int(tot_min_price), int(tot_max_price)):
        mp[price]+=('\t')

    # add max price as it will be ignored in for range loop above
    mp[tot_max_price] = '\t' + str(time_groups.index[current_time_group_index])[5:7] + '/' + str(time_groups.index[current_time_group_index])[3:4]

    for x in range(0, len(fin_prod_data)):
        if fin_prod_data.iloc[x]['date'] > time_groups.index[current_time_group_index]:
            # new time period
            char_mark=64
            # buffer and tab all entries
            buffer_max = max([len(v) for k,v in mp.items()])
            current_time_group_index += 1
            for k,v in mp.items():
                mp[k] += (chr(32) * (buffer_max - len(mp[k]))) + '\t'
            mp[tot_max_price] += str(time_groups.index[current_time_group_index])[5:7] + '/' + str(time_groups.index[current_time_group_index])[3:4]


        char_mark += 1
        min_price=fin_prod_data.iloc[x]['low']
        max_price=fin_prod_data.iloc[x]['high']
        for price in range(int(min_price), int(max_price)):
            mp[price]+=(chr(char_mark))
 
    sorted_keys = sorted(mp.keys(), reverse=True)
    for x in sorted_keys:
        # buffer each list
        print(str("{0:.2f}".format((x * 1.0) / height_precision)) + ': \t' + ''.join(mp[x]))
        result = str("{0:.2f}".format((x * 1.0) / height_precision)) + ': \t' + ''.join(mp[x])
        marketProfileResult[stockName].append(result)

    return marketProfileResult
 
def volume_profile(stockName, market_df, height_precision = 1, frequency='M'):
    df = market_df.copy()
    sub_df = df.loc[df['adjclose'].between(24, 25, inclusive=False)]

    sub_df.index.values

    start_price = df['adjclose'].min()
    stop_price = df['adjclose'].max()

    low = start_price
    # delta means granularity in volume aggregation range, it is delta in price
    # the volume corresponds to price
    delta = (stop_price - start_price)/100    # here we are splitting whole price range into blocks
    high = 0

    idx_array = []
    vol_array = []
    low_array = []

    while high < stop_price:
        volume = 0    
        high = low + delta
        
        sub_df = df.loc[df['adjclose'].between(low, high, inclusive=False)]
        low_array.append(low)

        for i in sub_df.index.values:
            print(i)
            print(df.iloc[i]['adjclose'])
            print(df.iloc[i]['volume'])
            volume = volume + df.iloc[i]['volume']
        print('total partial volume: ', volume)
                
        vol_array.append(volume)
        low = high

    print('final vol_array: ', vol_array)    
    
    for idx, var in enumerate(vol_array):
        print("{}: {}".format(idx, var))
        idx_array.append(idx)

    #minimum price
    print('start_price', start_price)

    #maximum price
    print('stop_price', stop_price)

    print(high)

# def volume_profile(df, price_pace=0.25, return_raw=False):
#     """
#     create volume profile
#     :param df: time-indexed HOLCV bar or time-indexed P-V tick
#     :param price_pace: price bucket, default 5 cents
#     :param return_raw: return raw data or figure
#     :return: raw data or figure obj
#     """

#     cmin = min(df['close'])
#     cmax = max(df['close'])
#     cmin_int = int(cmin / price_pace) * price_pace  # int(0.9) = 0
#     cmax_int = int(cmax / price_pace) * price_pace
#     if cmax_int < cmax:
#         cmax_int += price_pace
#     cmax_int += price_pace  # right bracket is not included in arrange

#     price_buckets = np.arange(cmin_int, cmax_int, price_pace)
#     price_coors = pd.Series(price_buckets).rolling(2).mean().dropna()
#     vol_bars = np.histogram(df.Close, bins=price_buckets, weights=df.Volume)[0]



  
