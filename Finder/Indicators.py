import numpy as np
from enum import Enum
import math
from termcolor import colored as cl 
from numpy.lib.function_base import average
import Enum.IndicatorEnum as ienum 
import Enum.CommonEnum as cenum
import pandas as pd

class Indicator:
    def sma(self, data, window):
        sma = data.rolling(window = window).mean()
        return sma

    # Exponentially-weighted Moving Average 
    def Esma(self, data, ndays):
        sma = data.ewm(span = ndays, min_periods = ndays - 1).mean()
        return sma

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