from email.policy import default
import Enum.CommonEnum as enum
import Enum.IndicatorEnum as ienum
import Finder.Pattern as pattern
import Finder.CandleStick as candle
import Finder.SupportResistence as sr
from datetime import datetime, timedelta
import Finder.BollingerBand as bband
import Finder.PeekHighLow as peekHL
from collections import defaultdict
import numpy as np
import Finder.RelativeStrengthIndex as rsi
import Utility.Constant as con
import Enum.MarketEnum as menum
import Enum.PatternEnum as penum

#https://medium.com/geekculture/candlestick-trading-a-full-guide-on-patterns-and-strategies-b1efcb98675c

def basedOn_Piercing_Dark_CloudSystem(prev_openPrice, prev_closePrice, openPrice, closePrice):
    signal = enum.Signal.NONE
    if pattern.isPiercingCloudCoverPattern(prev_openPrice, prev_closePrice, openPrice, closePrice):
        signal = enum.Signal.BUY    
    if signal == enum.Signal.NONE and pattern.isDarkCloudCoverPattern(prev_openPrice, prev_closePrice, openPrice, closePrice):
        signal = enum.Signal.SELL
    return signal

def basedOn_HammerCandleSys(openPrice, highPrice, lowPrice, closePrice):
    match candle.find_Hammer_Sys(openPrice, highPrice, lowPrice, closePrice):
        case enum.HammerCandleSys.Hammer | enum.HammerCandleSys.InvertedHammer:
            return enum.Signal.BUY
        case enum.HammerCandleSys.HangingMan:
            return enum.Signal.SELL
        #case _:
        case default:
            return enum.Signal.NONE

def basedOn_ThreeCandles(highPrice, prev1_highPrice, prev2_highPrice, prev3_highPrice):
    signal = enum.Signal.NONE
    if pattern.find_ThreeWhiteKnights(highPrice, prev1_highPrice, prev2_highPrice, prev3_highPrice):
        signal = enum.Signal.BUY
    elif pattern.find_ThreeBlackCrows(highPrice, prev1_highPrice, prev2_highPrice, prev3_highPrice):
        signal = enum.Signal.SELL
    return signal

def basedOn_StarCandleSys(openPrice, highPrice, closePrice, prev1_openPrice, prev1_highPrice, prev1_lowPrice, prev1_closePrice, prev2_openPrice, prev2_closePrice):
    signal = enum.Signal.NONE
    match candle.find_Star_Sys(openPrice, highPrice, closePrice, prev1_openPrice, prev1_highPrice, prev1_lowPrice, prev1_closePrice, prev2_openPrice, prev2_closePrice):
        case enum.StarCandleSys.MORNING:
            return enum.Signal.BUY
        case enum.StarCandleSys.EVENING:
            return enum.Signal.SELL
        #case _:
        case default:
            return enum.Signal.NONE

def basedOn_DojiCandleSys(openPrice, closePrice, prev_openPrice, prev_closePrice):
    signal = enum.Signal.NONE
    match candle.find_Doji_Sys(openPrice, closePrice, prev_openPrice, prev_closePrice):
        case enum.DojiCandleSys.BULL:
            return enum.Signal.BUY
        case enum.DojiCandleSys.BEAR:
            return enum.Signal.SELL
        #case _:
        case default:
            return enum.Signal.NONE 

def basedOn_MarubozuCandleSys(openPrice, highPrice, lowPrice, closePrice):
    signal = enum.Signal.NONE
    match candle.find_Marubozu_Sys(openPrice, highPrice, lowPrice, closePrice):
        case enum.MarubozuCandleSys.BULL:
            return enum.Signal.BUY
        case enum.MarubozuCandleSys.BEAR:
            return enum.Signal.SELL
        #case _:
        case default:
            return enum.Signal.NONE 

def basedOn_Harami_Pattern(openPrice, highPrice, lowPrice, closePrice, prev_openPrice, prev_closePrice):
    signal = enum.Signal.NONE
    match pattern.find_Harami_Pattern(openPrice, highPrice, lowPrice, closePrice, prev_openPrice, prev_closePrice):
        case enum.HaramiCandleSys.BULL:
            return enum.Signal.BUY
        case enum.HaramiCandleSys.BEAR:
            return enum.Signal.SELL
        #case _:
        case default:
            return enum.Signal.NONE 

def basedOn_ThreeSystem_Method(openPrice, closePrice, prev1_closePrice, prev1_openPrice, prev2_openPrice, prev2_closePrice, prev3_openPrice, prev3_closePrice, prev4_openPrice, prev4_closePrice):
    signal = enum.Signal.NONE
    match pattern.ThreeSystem_Method(openPrice, closePrice, prev1_closePrice, prev1_openPrice, prev2_openPrice, prev2_closePrice, prev3_openPrice, prev3_closePrice, prev4_openPrice, prev4_closePrice):
        case enum.ThreeSystem_Method.BULL:
            return enum.Signal.BUY
        case enum.ThreeSystem_Method.BEAR:
            return enum.Signal.SELL
        #case _:
        case default:
            return enum.Signal.NONE 

def basedOn_First_SupportResistence(supportresistence: sr, candle, trend, live_open_price, live_close_price):
    signal = enum.Signal.NONE
    if supportresistence.ready_at_enter == enum.SR_First_Method.BUY_AT_RESISTENCE or \
    supportresistence.ready_at_enter == enum.SR_First_Method.BUY_AT_SUPPORT:
        signal = enum.Signal.BUY
    elif supportresistence.ready_at_enter == enum.SR_First_Method.SELL:
        signal = enum.Signal.SELL
    return signal

def basedOnCandle(openPrice, closePrice): 
    signal = enum.Signal.NONE
    candl = candle.getCandleColor(openPrice, closePrice)
    if candl == enum.Candle.GREEN:
        signal = enum.Signal.BUY
    elif candl == enum.Candle.RED:
        signal = enum.Signal.SELL

    return signal

class Signal:
    __signals = defaultdict(list)
    #def __init__(self): 
        #self._signals = defaultdict(list)

    def __del__(self):
        #self.__signals.clear
        keylist = []
        if self.__signals != None:
            for signal in self.__signals:
                self.__signals[signal] = None
                keylist.append(signal)
            for key in keylist:
                self.__signals.pop(key)
        self.__signals = None

    def GetAllSignals(self):
        return self.__signals

    def __constructindicatoroutput(self, stockname, indicator, internal, signal, date, price, onDate = ""):
        on_date = onDate.strftime(con.DATE_FORMAT_YMD)

        if indicator == ienum.Indicators.BBAND.name:
            indicator = "Bollinger Band"
        elif indicator == ienum.Indicators.TREND.name:
            indicator = "Trend"
        elif indicator == ienum.Indicators.SUPPORTRESISTENCE.name:
            indicator = "Support And Resistence"
        elif indicator == ienum.Indicators.MOVINGAVERAGE20.name:
            indicator = "Moving Average 20"
        elif indicator == ienum.Indicators.RSI14_OverBoughtSold.name:
            indicator = "Relative strength index 14"
        elif indicator == ienum.Indicators.RSI14_DIVERGENCE.name:
            indicator = "Relative strength index 14 Divergence"

        indicator = indicator + " " + internal
        signal = {"Tool": indicator,"Signal" : signal, "Date": date, "Price": round(price,2), "OnDate": on_date}
        if not np.isnan(price):
            self.__signals[stockname].append(signal)

        return signal

    def basedOnBollingerBand2(self, stockname, stockData, onDate = "", internal= enum.Interval.NONE):

        bbandObject = bband.BollingerBand(stockData) 
        lastBBOverHighLowLevel = bbandObject.getLastOverHighLowLevel(onDate)

        result = {}

        signal = enum.Signal.NONE
        if lastBBOverHighLowLevel: 
            last_date = lastBBOverHighLowLevel.Date
            last_signal_date = last_date.strftime(con.DATE_FORMAT_YMD)
            if lastBBOverHighLowLevel.BB_OverHighLowLevel == ienum.BB_OverHighLowLevel.OVERHIGHLEVEL:
                signal = enum.Signal.SELL
            elif lastBBOverHighLowLevel.BB_OverHighLowLevel == ienum.BB_OverHighLowLevel.OVERLOWLEVEL:
                signal = enum.Signal.BUY
            result = self.__constructindicatoroutput(stockname, ienum.Indicators.BBAND.name, internal.name, \
                signal, last_signal_date, lastBBOverHighLowLevel.ClosePrice, onDate)   

        return result

    def basedOnBollingerBand(self, stockname, stockData, onDate = "", internal = enum.Interval.NONE):
        result = {}
        signal = enum.Signal.NONE

        if internal == enum.Interval.DAILY:
            bbandObject = bband.BollingerBand(stockData) 
            lastBBOverHighLowLevel = bbandObject.getLastOverHighLowLevel(onDate)
            if lastBBOverHighLowLevel: 
                last_date = lastBBOverHighLowLevel.Date
                last_signal_date = last_date.strftime(con.DATE_FORMAT_YMD)
                if lastBBOverHighLowLevel.BB_OverHighLowLevel == ienum.BB_OverHighLowLevel.OVERHIGHLEVEL:
                    signal = enum.Signal.SELL
                elif lastBBOverHighLowLevel.BB_OverHighLowLevel == ienum.BB_OverHighLowLevel.OVERLOWLEVEL:
                    signal = enum.Signal.BUY
                result = self.__constructindicatoroutput(stockname, ienum.Indicators.BBAND.name, internal.name, \
                    signal.name, last_signal_date, lastBBOverHighLowLevel.ClosePrice, onDate)   
            else:
                result = self.__constructindicatoroutput(stockname, ienum.Indicators.BBAND.name, internal.name, \
                    signal.name, "NONE", 0, onDate) 
        else:
            sma20 = stockData['sma_20'][len(stockData)-1]
            lowPrice = stockData['low'][len(stockData)-1]
            highPrice = stockData['high'][len(stockData)-1]
            openPrice = stockData['open'][len(stockData)-1]
            closePrice = stockData['close'][len(stockData)-1]
            latestDate = stockData['date'][len(stockData)-1]
            upper20_bb = stockData['upper20_bb'][len(stockData)-1]
            last_signal_date = latestDate.strftime(con.DATE_FORMAT_YMD)
            if closePrice > sma20:
                # if (internal == enum.Interval.MONTHLY and upper20_bb < highPrice) or candle.isBigRedCandle(openPrice, highPrice, lowPrice, closePrice):
                #     signal = enum.Signal.NONE
                # else:              
                signal = enum.Signal.BUY
            else:
                signal = enum.Signal.SELL
            result = self.__constructindicatoroutput(stockname, ienum.Indicators.BBAND.name, internal.name, \
                    signal.name, last_signal_date, closePrice, onDate)  

        return result

    def basedOnPeekHighLowTrend(self, stockname, stockData, peekHighLowTrendResult, onDate = "", internal= enum.Interval.NONE):
        latestPrice = stockData['close'][len(stockData)-1]
        latestDate = stockData['date'][len(stockData)-1]

        result = {}

        signal = enum.Signal.NONE
        if peekHighLowTrendResult != enum.Trend.NONE:            
            if peekHighLowTrendResult == enum.Trend.UP:
                signal = enum.Signal.BUY
            elif peekHighLowTrendResult == enum.Trend.DOWN:
                signal = enum.Signal.SELL
            
            signal_date = latestDate.strftime(con.DATE_FORMAT_YMD)           
            result = self.__constructindicatoroutput(stockname, ienum.Indicators.TREND.name, internal.name, \
                signal.name, signal_date, latestPrice, onDate)   

        return result
    
    def basedOnWickReversalPattern(self, stockname, stockData, peekHighLowTrendResult, onDate = "", internal= enum.Interval.NONE):
        latestClose = stockData['close'][len(stockData)-1]
        latestOpen = stockData['open'][len(stockData)-1]
        latestHigh = stockData['high'][len(stockData)-1]
        latestLow = stockData['low'][len(stockData)-1]
        latestDate = stockData['date'][len(stockData)-1]

        findPattern = pattern.findWickReversalPattern(latestOpen, latestHigh, latestLow, latestClose)

        result = {}

        signal = enum.Signal.NONE
        # if findPattern == menum.MarketType.MOREBULLISH or findPattern == menum.MarketType.MOREBEARISH:            
        #     if findPattern == menum.MarketType.MOREBULLISH:
        #         signal = enum.Signal.BUY
        #     elif findPattern == menum.MarketType.MOREBEARISH:
        #         signal = enum.Signal.SELL

        if findPattern != menum.MarketType.NONE:            
            if findPattern == menum.MarketType.MOREBULLISH or findPattern == menum.MarketType.BULLISH:
                signal = enum.Signal.BUY
            elif findPattern == menum.MarketType.MOREBEARISH or findPattern == menum.MarketType.BEARISH:
                signal = enum.Signal.SELL
            
            signal_date = latestDate.strftime(con.DATE_FORMAT_YMD)           
            result = self.__constructindicatoroutput(stockname, penum.ReversalPattern.WICKREVERSALPATTERN.name, internal.name, \
                signal.name, signal_date, latestClose, onDate) 

        return result
    
    def basedOnExtremeReversalPattern(self, stockname, stockData, onDate = "", internal= enum.Interval.NONE, takePrevCandles = 3):
        if len(stockData) > (1 + takePrevCandles):
            latestClose = stockData['close'][len(stockData)-1]
            latestOpen = stockData['open'][len(stockData)-1]
            latestHigh = stockData['high'][len(stockData)-1]
            latestLow = stockData['low'][len(stockData)-1]
            latestDate = stockData['date'][len(stockData)-1]

            prevClose = stockData['close'][len(stockData)-2]
            prevOpen = stockData['open'][len(stockData)-2]
            prevHigh = stockData['high'][len(stockData)-2]
            prevLow = stockData['low'][len(stockData)-2]

            totalBodyWidth = 0
            for p in range(1, takePrevCandles+1):
                takeOpen = stockData['open'][len(stockData)-(2+ p)]
                takeClose = stockData['close'][len(stockData)-(2+ p)]
                totalBodyWidth += candle.getWidth(takeOpen, takeClose)

            avgBodyWidth = totalBodyWidth/takePrevCandles

            findPattern = pattern.findExtremeReversalPattern(latestOpen, latestHigh, latestLow, latestClose, prevOpen, prevHigh, prevLow, prevClose, avgBodyWidth)
        else:
            findPattern = menum.MarketType.NONE

        result = {}

        signal = enum.Signal.NONE

        if findPattern != menum.MarketType.NONE:            
            if findPattern == menum.MarketType.BULLISH:
                signal = enum.Signal.BUY
            elif findPattern == menum.MarketType.BEARISH:
                signal = enum.Signal.SELL
            
            signal_date = latestDate.strftime(con.DATE_FORMAT_YMD)           
            result = self.__constructindicatoroutput(stockname, penum.ReversalPattern.EXTREMEREVERSALPATTERN.name, internal.name, \
                signal.name, signal_date, latestClose, onDate) 

        return result

    def basedOnOutsideReversalPattern(self, stockname, stockData, onDate = "", internal= enum.Interval.NONE, takePrevCandles = 3):
        if len(stockData) > (1 + takePrevCandles):
            latestClose = stockData['close'][len(stockData)-1]
            latestOpen = stockData['open'][len(stockData)-1]
            latestHigh = stockData['high'][len(stockData)-1]
            latestLow = stockData['low'][len(stockData)-1]
            latestDate = stockData['date'][len(stockData)-1]

            prevClose = stockData['close'][len(stockData)-2]
            prevOpen = stockData['open'][len(stockData)-2]
            prevHigh = stockData['high'][len(stockData)-2]
            prevLow = stockData['low'][len(stockData)-2]

            totalBodyWidth = 0
            for p in range(1, takePrevCandles+1):
                takeOpen = stockData['open'][len(stockData)-(2+ p)]
                takeClose = stockData['close'][len(stockData)-(2+ p)]
                totalBodyWidth += candle.getWidth(takeOpen, takeClose)

            avgBodyWidth = totalBodyWidth/takePrevCandles

            findPattern = pattern.findEngulfingPattern(latestOpen, latestHigh, latestLow, latestClose, prevOpen, prevHigh, prevLow, prevClose, avgBodyWidth)
        else:
            findPattern = menum.MarketType.NONE

        result = {}

        signal = enum.Signal.NONE

        if findPattern != menum.MarketType.NONE:            
            if findPattern == menum.MarketType.BULLISH:
                signal = enum.Signal.BUY
            elif findPattern == menum.MarketType.BEARISH:
                signal = enum.Signal.SELL
            
            signal_date = latestDate.strftime(con.DATE_FORMAT_YMD)           
            result = self.__constructindicatoroutput(stockname, penum.ReversalPattern.OUTSIDEREVERSALPATTERN.name, internal.name, \
                signal.name, signal_date, latestClose, onDate) 

        return result
    
    def basedOnDojiReversalPattern(self, stockname, stockData, onDate = "", internal= enum.Interval.NONE, takePrevCandles = 4):
        if len(stockData) > (1 + takePrevCandles):
            latestClose = stockData['close'][len(stockData)-1]
            latestOpen = stockData['open'][len(stockData)-1]
            latestHigh = stockData['high'][len(stockData)-1]
            latestLow = stockData['low'][len(stockData)-1]
            latestDate = stockData['date'][len(stockData)-1]

            prevClose = stockData['close'][len(stockData)-2]
            prevOpen = stockData['open'][len(stockData)-2]
            prevHigh = stockData['high'][len(stockData)-2]
            prevLow = stockData['low'][len(stockData)-2]

            prev2Close = stockData['close'][len(stockData)-3]
            prev2Open = stockData['open'][len(stockData)-3]
            prev2High = stockData['high'][len(stockData)-3]
            prev2Low = stockData['low'][len(stockData)-3]

            sma10 = stockData['sma_10'][len(stockData)-1]

            totalCandleWidth = 0
            for p in range(1, takePrevCandles+1):
                takeOpen = stockData['high'][len(stockData)-(2+ p)]
                takeClose = stockData['low'][len(stockData)-(2+ p)]
                totalCandleWidth += candle.getWidth(takeOpen, takeClose)

            avgCandleWidth = totalCandleWidth/takePrevCandles

            findPattern = pattern.findDojiReversalPattern(latestOpen, latestHigh, latestLow, latestClose, prevOpen, prevHigh, prevLow, prevClose, prev2Open, prev2High, prev2Low, prev2Close, avgCandleWidth, sma10)
        else:
            findPattern = menum.MarketType.NONE

        result = {}

        signal = enum.Signal.NONE

        if findPattern != menum.MarketType.NONE:            
            if findPattern == menum.MarketType.BULLISH:
                signal = enum.Signal.BUY
            elif findPattern == menum.MarketType.BEARISH:
                signal = enum.Signal.SELL
            
            signal_date = latestDate.strftime(con.DATE_FORMAT_YMD)           
            result = self.__constructindicatoroutput(stockname, penum.ReversalPattern.DOJIREVERSALPATTERN.name, internal.name, \
                signal.name, signal_date, latestClose, onDate) 

        return result

    def basedOnPeekHighLowSR(self, stockname, stockData, peekHighLowSR, onDate="", internal=enum.Interval.NONE):
        latestPrice = stockData['close'][len(stockData)-1]
        latestDate = stockData['date'][len(stockData)-1]

        signal = enum.Signal.NONE
        if peekHighLowSR:
            if peekHighLowSR.SRLevel == enum.SRLevel.SUPPORT:
                if latestPrice > peekHighLowSR.HighPrice:
                    signal = enum.Signal.BUY
            elif peekHighLowSR.SRLevel == enum.SRLevel.RESISTENCE:  
                if latestPrice < peekHighLowSR.LowPrice:
                    signal = enum.Signal.SELL

        result = {}
        signal_date = latestDate.strftime(con.DATE_FORMAT_YMD)
        result = self.__constructindicatoroutput(stockname, ienum.Indicators.SUPPORTRESISTENCE.name, internal.name, \
            signal.name, signal_date, latestPrice, onDate)   

        return result

    def basedOnMovingAverage20(self, stockname, stockData, lastPeekHLLevel, onDate="", internal=enum.Interval.NONE):
        result = {}
        
        if lastPeekHLLevel != None:
            latestPrice = stockData['close'][len(stockData)-1]
            latestDate = stockData['date'][len(stockData)-1]

            sma_20 = stockData['sma_20'][len(stockData)-1]
            signal = enum.Signal.NONE
            if latestPrice > sma_20 and lastPeekHLLevel.SMA_20 > lastPeekHLLevel.HighPrice:
                signal = enum.Signal.BUY
            elif latestPrice < sma_20 and lastPeekHLLevel.SMA_20 < lastPeekHLLevel.LowPrice:
                signal = enum.Signal.SELL
            
            signal_date = latestDate.strftime(con.DATE_FORMAT_YMD)
            result = self.__constructindicatoroutput(stockname, ienum.Indicators.MOVINGAVERAGE20.name, internal.name, \
                signal.name, signal_date, latestPrice, onDate) 

        return result

    def basedOnRelativeStrenghtIndex14(self, stockname, stockData, onDate="", internal=enum.Interval.NONE):
        rsicall = rsi.RelativeStrengthIndex(stockData, trendCountCheck = 0)
        lastOverBoughtSold = rsicall.getLastOverBoughtSoldPeekLevel()

        result = {}
        
        if lastOverBoughtSold != None:
            lastOverBoughtSoldDate = lastOverBoughtSold.Date
            lastOverBoughtSoldPrice = lastOverBoughtSold.ClosePrice

            latestPrice = stockData['close'][len(stockData)-1]
            latestDate = stockData['date'][len(stockData)-1]

            signal = enum.Signal.NONE
            #checking last 5 days
            if latestDate <= lastOverBoughtSoldDate + timedelta(5):
                if lastOverBoughtSold.OverBoughtSold == enum.OverBoughtSold.OVERSOLD:
                    signal = enum.Signal.BUY
                elif lastOverBoughtSold.OverBoughtSold == enum.OverBoughtSold.OVERBOUGHT:
                    signal = enum.Signal.SELL           

            signal_date = lastOverBoughtSoldDate.strftime(con.DATE_FORMAT_YMD)
            result = self.__constructindicatoroutput(stockname, ienum.Indicators.RSI14_OverBoughtSold.name, internal.name, \
                signal.name, signal_date, lastOverBoughtSoldPrice, onDate) 

        return result

    def basedOnRSI14DivergenceLevel(self, stockname, stockData, onDate="", internal=enum.Interval.NONE):
        rsicall = rsi.RelativeStrengthIndex(stockData, trendCountCheck = 0)
        lastRSIDivergencePoints = rsicall.getLastDivergencePoints()

        result = {}
        
        if lastRSIDivergencePoints:
            lastRSIDivergenceDate = lastRSIDivergencePoints.Date
            lastRSIDivergencePrice = lastRSIDivergencePoints.ClosePrice

            latestPrice = stockData['close'][len(stockData)-1]
            latestDate = stockData['date'][len(stockData)-1]

            signal = enum.Signal.NONE
            #checking last 30*2 days
            if latestDate <= lastRSIDivergenceDate + timedelta(30*2):
                if lastRSIDivergencePoints.DivergenceLevel == enum.DivergenceLevel.BEARISH:
                    signal = enum.Signal.BUY
                elif lastRSIDivergencePoints.DivergenceLevel == enum.DivergenceLevel.BULLISH:
                    signal = enum.Signal.SELL

            if signal != enum.Signal.NONE:
                signal_date = lastRSIDivergenceDate.strftime(con.DATE_FORMAT_YMD)
            else:
                signal_date = latestDate.strftime(con.DATE_FORMAT_YMD)
            result = self.__constructindicatoroutput(stockname, ienum.Indicators.RSI14_DIVERGENCE.name, internal.name, \
                signal.name, signal_date, lastRSIDivergencePrice, onDate) 

        return result