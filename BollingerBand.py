import numpy as np
from enum import Enum
import math
from termcolor import colored as cl 
from numpy.lib.function_base import average

class BreakOut(Enum):
  UPPER_BB = 1
  LOWER_BB = 2
  NONE = 0

class InLine(Enum):
  UPPER_BB_LINE = 1,
  LOWER_BB_LINE = 2,
  SMA_LINE = 3,
  NONE = 0

def sma(data, window):
    sma = data.rolling(window = window).mean()
    return sma

def bb(data, sma, window):
    std = data.rolling(window = window).std()
    upper_bb = sma + std * 2
    lower_bb = sma - std * 2
    return upper_bb, lower_bb

def break_out(stock):
    line_at = []
    breakout_at = []
    for i in range(len(stock)):
        lower_bb = stock['lower_bb'][i]
        upper_bb = stock['upper_bb'][i]
        sma = stock['sma_20'][i]
        high_price = stock['high'][i]
        low_price = stock['low'][i]
    

        break_out_at = BreakOut.NONE
        in_line_at = InLine.NONE

        if (high_price >= lower_bb >= low_price):
            in_line_at = InLine.LOWER_BB_LINE
        elif (high_price <= upper_bb <= low_price):
            in_line_at = InLine.UPPER_BB_LINE
        elif (high_price < lower_bb):
            break_out_at = BreakOut.LOWER_BB
        elif (low_price > upper_bb):
            break_out_at = BreakOut.UPPER_BB

        if (high_price >= sma >= low_price):
            in_line_at = InLine.SMA_LINE

        line_at.append(in_line_at)
        breakout_at.append(break_out_at)
        
    stock['in_line_at'] = line_at
    stock['break_out_at'] = breakout_at

def implement_bb_strategy(stock, signal_for):
    data = stock['close']
    lower_bb = stock['lower_bb']
    upper_bb = stock['upper_bb']
    buy_price = []
    prev_buy_price = 0
    sell_price = []
    bb_signal = []
    buy_date = []
    sell_date = []
    signal = 0
    prev_line_at = InLine.NONE
    temp_prev_line_at = InLine.NONE

    break_out_lower_bb = 0
    
    for i in range(len(data)):
        if temp_prev_line_at != InLine.NONE:
           prev_line_at = temp_prev_line_at
        if data[i-1] > lower_bb[i-1] and data[i] < lower_bb[i]:
            #if signal != 1:
            if (prev_line_at == InLine.SMA_LINE):
                buy_price.append(data[i])
                prev_buy_price = data[i]
                sell_price.append(np.nan)
                signal = 1
                signal_for = 0
                bb_signal.append(signal)
                buy_date.append(data.index[i])
            else:
                buy_price.append(np.nan)
                sell_price.append(np.nan)
                bb_signal.append(0)
        elif data[i-1] < upper_bb[i-1] and data[i] > upper_bb[i]:
            #if signal != -1 and signal_for == 0 :
            if signal_for == 0 :
                buy_price.append(np.nan)
                sell_price.append(data[i])
                signal = -1
                bb_signal.append(signal)
                sell_date.append(data.index[i])
            else:
                buy_price.append(np.nan)
                sell_price.append(np.nan)
                bb_signal.append(0)
        else:
            buy_price.append(np.nan)
            sell_price.append(np.nan)
            bb_signal.append(0)
        temp_prev_line_at = stock['in_line_at'][i]
            
    return buy_price, sell_price, bb_signal, buy_date, sell_date

def calculateProfit(buy_price, sell_price, bb_signal, stock, ticket):
    profit = 0
    buyAmt = []
    avgbuyAmt = 0
    sellAmt = 0
            
    for i in range(len(bb_signal)):
        if bb_signal[i] == 1:
            buyAmt.append(buy_price[i])
        #elif bb_signal[i] == -1:
            #sellAmt = sell_price[i]
            
    sellAmt = stock['close'][len(stock)-1]
    result = 0
    amount = 0
    share = 0

    if len(buyAmt) > 0:
        avgbuyAmt = average(buyAmt)
        investment_value = 10000
        number_of_stocks = math.floor(investment_value/avgbuyAmt)

        profit = (sellAmt - avgbuyAmt)

        returns = number_of_stocks*profit

        profit_percentage = math.floor((returns/investment_value)*100)
        result = profit_percentage
        amount = returns
        share = 1
        print('*'+ str(ticket) +'*' + cl('Profit percentage of the BB strategy : {}%'.format(profit_percentage), attrs = ['bold']))
    return result, amount, share