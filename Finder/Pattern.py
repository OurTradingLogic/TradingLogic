from signal import signal
import Finder.CandleStick as candle
import Enum.CommonEnum as enum

def isPiercingCloudCoverPattern(prev_openPrice, prev_closePrice, openPrice, closePrice):
    #closePrice < prev_openPrice and closePrice > prev_closePrice and openPrice < prev_closePrice and \ will move seperate method later
    return candle.getCandleColor(openPrice, closePrice) == enum.Candle.GREEN and candle.getCandleColor(prev_openPrice, prev_closePrice) == enum.Candle.RED and \
       closePrice < prev_openPrice and closePrice > prev_closePrice and openPrice < prev_closePrice and \
       candle.getTrend(prev_openPrice, prev_closePrice, closePrice) == enum.Trend.UP

def isDarkCloudCoverPattern(prev_openPrice, prev_closePrice, openPrice, closePrice):
    #closePrice > prev_openPrice and closePrice < prev_closePrice and openPrice > prev_closePrice and \ will move seperate method later
    return candle.getCandleColor(openPrice, closePrice) == enum.Candle.RED and candle.getCandleColor(prev_openPrice, prev_closePrice) == enum.Candle.GREEN and \
       closePrice > prev_openPrice and closePrice < prev_closePrice and openPrice > prev_closePrice and \
       candle.getTrend(prev_openPrice, prev_closePrice, closePrice) == enum.Trend.DOWN

def find_ThreeWhiteKnights(highPrice, prev1_highPrice, prev2_highPrice, prev3_highPrice):
    # Three White Soldiers
    return highPrice > prev1_highPrice and \
        prev1_highPrice > prev2_highPrice and \
        prev2_highPrice > prev3_highPrice

def find_ThreeBlackCrows(highPrice, prev1_highPrice, prev2_highPrice, prev3_highPrice):
    # Three Black Crows
    return highPrice < prev1_highPrice and \
        prev1_highPrice < prev2_highPrice and \
        prev2_highPrice < prev3_highPrice

def find_Harami_Pattern(openPrice, highPrice, lowPrice, closePrice, prev_openPrice, prev_closePrice):
    result = enum.HaramiCandleSys.NONE
    if candle.candle.isRed(prev_openPrice, prev_closePrice) and \
        candle.candle.isGreen(openPrice, closePrice) and \
        prev_closePrice < lowPrice and \
        prev_openPrice > highPrice:
        result = enum.HaramiCandleSys.BULL           
    elif candle.candle.isGreen(prev_openPrice, prev_closePrice) and \
        candle.candle.isRed(openPrice, closePrice) and \
        prev_closePrice > highPrice and \
        prev_openPrice < lowPrice:
        result = enum.HaramiCandleSys.BEAR
    return result

#where a candle is followed by three candles of the other color which are in turn followed by a candle of the same color as the first one. 
# The three candles in the middle should be contained within the ranges of the other two.
def find_ThreeSystem_Method(openPrice, closePrice, prev1_closePrice, prev1_openPrice, prev2_openPrice, prev2_closePrice, prev3_openPrice, prev3_closePrice, prev4_openPrice, prev4_closePrice):
    result = enum.ThreeSystem_Method.NONE
    # Bullish Strike Method
    if candle.isGreen(openPrice, closePrice): 
        if candle.isRed(prev1_openPrice, prev1_closePrice) and candle.isRed(prev2_openPrice, prev2_closePrice) and \
        candle.isRed(prev3_openPrice, prev3_closePrice) and candle.isGreen(prev4_openPrice, prev4_closePrice) and closePrice > prev3_openPrice and \
        prev4_openPrice < prev1_closePrice and prev1_closePrice < prev2_closePrice and prev2_closePrice < prev3_closePrice:
            result = enum.ThreeSystem_Method.BULL
    # Bearish Strike Method
    elif candle.isRed(openPrice, closePrice): 
        if candle.isGreen(prev1_openPrice, prev1_closePrice) and candle.isGreen(prev2_openPrice, prev2_closePrice) and \
        candle.isGreen(prev3_openPrice, prev3_closePrice) and candle.isRed(prev4_openPrice, prev4_closePrice) and closePrice < prev3_openPrice and \
        prev4_openPrice > prev1_closePrice and prev1_closePrice > prev2_closePrice and prev2_closePrice > prev3_closePrice:
            result = enum.ThreeSystem_Method.BEAR
    return result