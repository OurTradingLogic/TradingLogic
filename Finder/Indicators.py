import numpy as np
from enum import Enum
import math
from termcolor import colored as cl 
from numpy.lib.function_base import average
import Enum.IndicatorEnum as ienum 
import Enum.CommonEnum as cenum
import pandas as pd
import json

class Indicator:
    def __init__(self, jsonData = ""):
        self._jsonData = jsonData

    def get(self):
        all_list = [] #empty list
        if self._jsonData != "":
            #jstr = "{\"StockList\":[{\"Symbol\":\"AEGISCHEM\",\"Exchange\":\"NSE\"}],\"SignalList\":[{\"Name\":\"Bollinger Band\",\"Code\":\"NA\"}]}"
            load = json.loads(self._jsonData)

            for data in load["SignalList"]:    
                #indicator = str(data['Name'])
                code = str(data['Code'])
                all_list.append(code)
        else:
            for indicator in ienum.Indicators:
                all_list.append(indicator.name)

        return all_list

    def sma(self, close, window):
        sma = close.rolling(window = window).mean()
        return sma

    # Exponentially-weighted Moving Average 
    def Esma(self, close, ndays):
        sma = close.ewm(span = ndays, min_periods = ndays - 1).mean()
        return sma
    
    def MACD(self, close, periodexp1 = 12, periodexp2 = 26):
        exp1 = close.ewm(span=periodexp1, adjust=False).mean()
        exp2 = close.ewm(span=periodexp2, adjust=False).mean()
        return exp1 - exp2
    
    def SingleLineMACD(self, close, periodexp1 = 9):
        exp1 = close.ewm(span=periodexp1, adjust=False).mean()
        return exp1
    
    def StochasticOscillator(self, data, window = 14):
        high = data['high'].rolling(window).max()
        low = data['low'].rolling(window).min()
        #14-high: Maximum of last 14 trading days
        #14-low: Minimum of last 14 trading days
        #%K: (Last Close – 14-low)*100 / (14-high – 14-low)
        #%D: Simple Moving Average of %K
        kData = (data['close'] - low)*100/(high - low)
        dData = self.sma(kData, 3)
        return kData, dData

    def bb(self, data, sma, window):
        std = data.rolling(window = window).std()
        upper_bb = sma + std * 2
        lower_bb = sma - std * 2
        return upper_bb, lower_bb

    def rsi(self, close, periods = 14):   
        change = close.diff()
        change.dropna(inplace=True)

        # Create two copies of the closing price
        change_up = change.copy()
        change_down = change.copy()

        # up have 0 to n; down have 0 to -n
        change_up[change_up<0] = 0
        change_down[change_down>0] = 0

        # Verify that we did not make any mistakes
        #change.equals(change_up+change_down)
        # Calculate the rolling average of average up and average down
        #avg_up = change_up.rolling(window = periods).mean()
        #avg_down = change_down.rolling(window = periods).mean().abs()
        #rsi = 100 * avg_up / (avg_up + avg_down)
        #relative_strength = avg_up/avg_down
        #rsi = 100.0 - (100.0 / (1.0 + relative_strength))

        avg_up = change_up.ewm(com = periods-1, adjust=False).mean()
        avg_down = abs(change_down.ewm(com = periods-1, adjust=False).mean())
        #rsi = 100 * avg_up / (avg_up + avg_down)
        relative_strength = avg_up/avg_down
        rsi = 100 - 100 / (1 + relative_strength)

        return rsi
    
    #TR = ​max [(high − low), abs(high − closeprev​), abs(low – closeprev​)]
    def trueRange(self, data):
        h_l = data['high'] - data['low']
        h_cp = np.abs(data['high'] - data['close'].shift())
        l_cp = np.abs(data['low'] - data['close'].shift())
        ranges = pd.concat([h_l, h_cp, l_cp], axis=1)
        return np.max(ranges, axis=1)

    def averageTrueRange(self, data, window = 14):
        true_range = self.trueRange(data)
        #return true_range.rolling(window).mean()
        return true_range.rolling(window).sum()/window

    def super_trend(self, df, period=10, multiplier=3):
        hl_avg = (df['high'] + df['low']) / 2
        average_true_range = self.averageTrueRange(df, period)
        
        up = hl_avg + multiplier * average_true_range
        down = hl_avg - multiplier * average_true_range
        
        # df['Trend'] = 0
        # df['Trend'] = df['Trend'].mask(df['close'] > up, 1)
        # df['Trend'] = df['Trend'].mask(df['close'] < down, -1)
        
        # prev_trend = 0
        # for i in range(1, len(df)):
        #     if df['Trend'].iloc[i] == 0:
        #         df['Trend'].iloc[i] = prev_trend
        #     else:
        #         prev_trend = df['Trend'].iloc[i]
        
        # df['SuperTrend'] = hl_avg + (multiplier * average_true_range * df['Trend'])
        return up, down

    def generate_signals(self, df):
        signals = []
        prev_signal = 0
        
        for i in range(1, len(df)):
            curr_signal = 0
            
            if df['close'].iloc[i] > df['SuperTrend'].iloc[i]:
                curr_signal = 1  # Buy signal
            elif df['close'].iloc[i] < df['SuperTrend'].iloc[i]:
                curr_signal = -1  # Sell signal
            
            if curr_signal != prev_signal:
                signals.append(curr_signal)
            else:
                signals.append(0)
            
            prev_signal = curr_signal
        
        df['Signal'] = signals
        return df

    def loadBasic(self, df):
        df['sma_20'] = self.sma(df.close, 20)
        df['upper20_bb'], df['lower20_bb'] = self.bb(df['close'], df['sma_20'], 20)
        df['rsi_14'] = self.rsi(df['close'], 14)
        df['atr'] = self.averageTrueRange(df)
        df['macd'] = self.MACD(df['close'])
        df['smacd'] = self.SingleLineMACD(df['close'])

        # super_trend_data = self.calculate_super_trend(df)
        # signal_data = self.generate_signals(super_trend_data)
        # print(signal_data[['date', 'close', 'SuperTrend', 'Signal']])
