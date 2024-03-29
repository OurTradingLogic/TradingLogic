import numpy as np
from enum import Enum
import math
from termcolor import colored as cl 
from numpy.lib.function_base import average
import Enum.IndicatorEnum as ienum 
import Enum.CommonEnum as cenum
import Model.FinderModel as fmodel

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


class BollingerBand:
    def __init__(self, data):
        self.__bband_list = []
        self.__load(data)

    def __del__(self):
        self.__bband_list.clear()

    def __load(self,data):
        self.__load_bb20(data)      

    def __load_bb20(self, stock):   
        bband_list = []
        prev_low_price = 0

        for i in range(len(stock)):

            if np.isnan(stock['sma_20'][i]):
                continue

            date = stock['date'][i]
            lower_bb = stock['lower20_bb'][i]
            upper_bb = stock['upper20_bb'][i]
            sma20 = stock['sma_20'][i]
            high_price = stock['high'][i]
            low_price = stock['low'][i]
            close_price = stock['close'][i]
            open_price = stock['open'][i]
            bb_BreakOut = ienum.BB_BreakOut.NONE
            bb_InLine = ienum.BB_InLine.NONE
            bb_OverHighLowLevel = ienum.BB_OverHighLowLevel.NONE

            prev_close_price = stock['close'][i-1]
            prev_lower_bb = stock['lower20_bb'][i-1]
            prev_upper_bb = stock['upper20_bb'][i-1]

            if (high_price >= lower_bb >= low_price):
                bb_InLine = ienum.BB_InLine.LOWER_BB_LINE
            elif (high_price <= upper_bb <= low_price):
                bb_InLine = ienum.BB_InLine.UPPER_BB_LINE
            elif (high_price < lower_bb):
                bb_BreakOut = ienum.BB_BreakOut.LOWER_BB
            elif (low_price > upper_bb):
                bb_BreakOut = ienum.BB_BreakOut.UPPER_BB

            if close_price > open_price:
                if (close_price >= sma20 >= open_price):
                    bb_InLine = ienum.BB_InLine.SMA_LINE
            elif (open_price >= sma20 >= close_price):
                    bb_InLine = ienum.BB_InLine.SMA_LINE

            if (prev_close_price > prev_lower_bb and close_price < lower_bb) or (open_price < lower_bb):
                #if prev_low_price == 0 or high_price >= prev_low_price: #Gap
                bb_OverHighLowLevel = ienum.BB_OverHighLowLevel.OVERLOWLEVEL
            elif prev_close_price < prev_upper_bb and close_price > upper_bb:
                bb_OverHighLowLevel = ienum.BB_OverHighLowLevel.OVERHIGHLEVEL
            
            if bb_InLine != ienum.BB_InLine.NONE or bb_BreakOut != ienum.BB_BreakOut.NONE or bb_OverHighLowLevel != ienum.BB_OverHighLowLevel.NONE:
                bband_list.append(fmodel.BollingerBandModel(date, high_price, low_price, close_price, open_price, upper_bb, lower_bb, sma20, bb_BreakOut, bb_InLine, bb_OverHighLowLevel))

            prev_low_price = low_price
        
        self.__bband_list = bband_list      

    def getOverHighLowLevels(self):
        if self.__bband_list:
            overHighLowList =  [item for item in self.__bband_list if item.BB_OverHighLowLevel == ienum.BB_OverHighLowLevel.OVERLOWLEVEL or \
                item.BB_OverHighLowLevel == ienum.BB_OverHighLowLevel.OVERHIGHLEVEL] 
            return overHighLowList
        return None

    def getLastOverHighLowLevel(self, date):
        overHighLowLevels= self.getOverHighLowLevels()
        if not overHighLowLevels:
            return None

        if date != None or date != "":
            bband_List = [item for item in overHighLowLevels if item.Date <= date] 
        else:
            bband_List = overHighLowLevels

        if bband_List:
            return bband_List[-1]
        else:
            return None

    def getBreakOutLevels(self):
        if self.__bband_list:
            bbBreakOutist =  [item for item in self.__bband_list if item.BB_BreakOutLevel == ienum.BB_BreakOut.LOWER_BB or \
                item.BB_BreakOutLevel == ienum.BB_BreakOut.UPPER_BB] 
            return bbBreakOutist
        return None

    def getBBInLineLevels(self):
        if self.__bband_list:
            bbBreakOutist =  [item for item in self.__bband_list if item.BB_InLineLevel == ienum.BB_InLine.LOWER_BB_LINE or \
                item.BB_InLineLevel == ienum.BB_InLine.UPPER_BB_LINE or item.BB_InLineLevel == ienum.BB_InLine.SMA_LINE] 
            return bbBreakOutist
        return None

    def findBollingerBandTrend(self, checkDate, iCheckCount = 2):
        iLowLevelCount = 0
        iHighLevelCount = 0
        trend = cenum.Trend.NONE       

        if checkDate != None:
            bband_List = [item for item in self.__bband_list if item.Date <= checkDate] 
        else:
            bband_List = self.__bband_list

        iCheckStarted = False
        iLoopCount = 0
        for bbModel in bband_List: 
            if not iCheckStarted:
                if bbModel.BB_OverHighLowLevel == ienum.BB_InLine.SMA_LINE:
                    continue
                else:
                    iCheckStarted = True

            iLoopCount+=1

            if iLoopCount > 2:
                break

            overHighLowLevel = bbModel.BB_OverHighLowLevel
            if overHighLowLevel == ienum.BB_OverHighLowLevel.OVERLOWLEVEL:
                iLowLevelCount+=1
                iHighLevelCount = 0
            elif overHighLowLevel == ienum.BB_OverHighLowLevel.OVERHIGHLEVEL:
                iHighLevelCount+=1
                iLowLevelCount == 0
            else:
                iLowLevelCount = 0
                iHighLevelCount = 0

            if iLowLevelCount == iCheckCount:
                trend = cenum.Trend.DOWN
            elif iHighLevelCount == iCheckCount:
                trend = cenum.Trend.UP
            
        return trend



def find_bb20_break_out(stock):
    stock['in_line_at'] = np.nan
    stock['break_out_at'] = np.nan
    for i in range(len(stock)):
        break_out_at = ienum.BB_BreakOut.NONE
        in_line_at = ienum.BB_InLine.NONE

        if np.isnan(stock['sma_20'][i]):
            continue

        lower_bb = stock['lower20_bb'][i]
        upper_bb = stock['upper20_bb'][i]
        sma20 = stock['sma_20'][i]
        high_price = stock['high'][i]
        low_price = stock['low'][i]

        if (high_price >= lower_bb >= low_price):
            in_line_at = ienum.BB_InLine.LOWER_BB_LINE
        elif (high_price <= upper_bb <= low_price):
            in_line_at = ienum.BB_InLine.UPPER_BB_LINE
        elif (high_price < lower_bb):
            break_out_at = ienum.BB_BreakOut.LOWER_BB
        elif (low_price > upper_bb):
            break_out_at = ienum.BB_BreakOut.UPPER_BB

        if (high_price >= sma20 >= low_price):
            in_line_at = ienum.BB_InLine.SMA_LINE
        
        stock['in_line_at'][i] = in_line_at
        stock['break_out_at'][i] = break_out_at

def implement_bb20_strategy(stock):
    stock_bb = stock

    find_bb20_break_out(stock_bb)
    date = stock_bb['date']
    closeprice = stock_bb['close']
    sma20 = stock_bb['sma_20']
    lower_bb = stock_bb['lower20_bb']
    upper_bb = stock_bb['upper20_bb']
    stock_bb['signal_bb'] = np.nan

    prev_line_at = ienum.BB_InLine.NONE
    temp_prev_line_at = ienum.BB_InLine.NONE
    
    result = []
    for i in range(len(closeprice)):
        if np.isnan(sma20[i]):
            continue
        if temp_prev_line_at != ienum.BB_InLine.NONE:
           prev_line_at = temp_prev_line_at
        if closeprice[i-1] > lower_bb[i-1] and closeprice[i] < lower_bb[i] and (prev_line_at == ienum.BB_InLine.SMA_LINE):
            stock_bb['signal_bb'][i] = cenum.Signal.BUY.name
            result.append({"date": date[i], "close": closeprice[i], "signal": cenum.Signal.BUY.name})
        elif closeprice[i-1] < upper_bb[i-1] and closeprice[i] > upper_bb[i]:
            stock_bb['signal_bb'][i] = cenum.Signal.SELL.name
            result.append({"date": date[i], "close": closeprice[i], "signal": cenum.Signal.SELL.name})

        temp_prev_line_at = stock_bb['in_line_at'][i]
            
    return result

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