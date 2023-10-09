from signal import signal
import Finder.CandleStick as candle
import Enum.CommonEnum as enum
import Enum.MarketEnum as mEnum
import Utility.Common as mCom

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

#if minimum wick ratio is 2 times. if it is higher, then more possibility for reversal
# personal comment: this is hamper candle
#1. A wick that is between 2.5 to 3.5 times larger than the size of the body.
#2. For a bullish reversal wick to exist, the close of the bar should fall within the top 35 percent of the overall range of the candle
#3. For a bearish reversal wick to exist, the close of the bar should fall within the bottom 35 percent of the overall range of the candle
def findWickReversalPattern(openPrice, highPrice, lowPrice, closePrice, wickLengthRatio = 2):
    body = candle.getWidth(openPrice, closePrice)
    #candleWidth = candle.getWidth(highPrice, lowPrice)
    #closeTailWidth = candle.getCloseTailWidth(openPrice, highPrice, lowPrice, closePrice)
    lower_tail = candle.getLowerTailWidth(openPrice, lowPrice, closePrice)
    upper_tail = candle.getUpperTailWidth(openPrice, highPrice, closePrice)
    wick = body * wickLengthRatio
    #closeTailPercent = mCom.PercentageBy(closeTailWidth, candleWidth)

    result = mEnum.MarketType.NONE
    #Green Candle
    if closePrice > openPrice:
        if lower_tail > wick: 
            topTailPercent = mCom.FindDifferencePercentage(upper_tail, body)
            if topTailPercent <= 5:
                result = mEnum.MarketType.MOREBULLISH 
        elif upper_tail > wick:
            bottomTailPercent = mCom.FindDifferencePercentage(lower_tail, body)
            if bottomTailPercent <= 35:
                result = mEnum.MarketType.BEARISH 
    #Red Candle
    elif closePrice < openPrice and upper_tail > wick: 
        if upper_tail > wick: 
            bottomTailPercent = mCom.FindDifferencePercentage(lower_tail, body)
            if bottomTailPercent <= 5:
                result = mEnum.MarketType.MOREBEARISH 
        elif lower_tail > wick:
            topTailPercent = mCom.FindDifferencePercentage(upper_tail, body)
            if topTailPercent <= 35:
                result = mEnum.MarketType.BULLISH 

    return result

#prev bar is about 2 times larger than average size in the loopback period
#prev bar body 50 percent large, not more than 85
#current bar should be opposite sign
def findExtremeReversalPattern(openPrice, highPrice, lowPrice, closePrice, prev_openPrice, prev_highPrice, prev_lowPrice, prev_closePrice, avgPrevBodySize):
    prev_bodyWidth = candle.getWidth(prev_openPrice, prev_closePrice)
    prev_candleWidth = candle.getWidth(prev_highPrice, prev_lowPrice)

    diffWithPrev = mCom.FindNDifference(prev_bodyWidth, avgPrevBodySize)
    bodyPercent = mCom.FindDifferencePercentage(prev_bodyWidth, prev_candleWidth)
    #bobyPercentWithTail = candle.getBobyPercentWithTail(openPrice, highPrice, lowPrice, closePrice)   

    prev_candle_result = mEnum.MarketType.NONE
    if diffWithPrev > 2 and bodyPercent > 50 and bodyPercent < 86: 
        prev_candleColor = candle.getCandleColor(prev_openPrice, prev_closePrice)
        if prev_candleColor == enum.Candle.GREEN:
            prev_candle_result = mEnum.MarketType.BULLISH 
        elif prev_candleColor == enum.Candle.RED:
            prev_candle_result = mEnum.MarketType.BEARISH 

    result = mEnum.MarketType.NONE
    if prev_candle_result == mEnum.MarketType.BULLISH:
        candleColor = candle.getCandleColor(openPrice, closePrice)
        if candleColor == enum.Candle.RED:
            result = mEnum.MarketType.BEARISH
    elif prev_candle_result == mEnum.MarketType.BEARISH:
        candleColor = candle.getCandleColor(openPrice, closePrice)
        if candleColor == enum.Candle.GREEN:
            result = mEnum.MarketType.BULLISH

    return result

#Also call as OutsideReversal Pattern
#the market will push price lower before shooting higher, and will push price higher before selling off
#1. engulfing bar is usually 5 to 25 percent larger than the size of average lookback period
#2. engulfing bar of a bullish bar has a low that is below the prior bar's low and a close that is above the prior bar's high
#3. engulfing bar of a bearish bar has a high that is above the prior bar's high and a close that is below the prior bar's low
def findEngulfingPattern(openPrice, highPrice, lowPrice, closePrice, prev_openPrice, prev_highPrice, prev_lowPrice, prev_closePrice, avgPrevBodySize):
    bodyWidth = candle.getWidth(openPrice, closePrice)
    candleWidth = candle.getWidth(highPrice, lowPrice)

    diffWithPrev = mCom.PercentageBy(bodyWidth, avgPrevBodySize)
    bodyPercent = mCom.FindDifferencePercentage(bodyWidth, candleWidth)
    #bobyPercentWithTail = candle.getBobyPercentWithTail(openPrice, highPrice, lowPrice, closePrice)   

    result = mEnum.MarketType.NONE

    if diffWithPrev > 5 and diffWithPrev < 26 and bodyPercent > 50: 
        candleColor = candle.getCandleColor(openPrice, closePrice)
        if candleColor == enum.Candle.GREEN:
            if lowPrice < prev_lowPrice and closePrice > prev_highPrice:
                result = mEnum.MarketType.BULLISH 
        elif candleColor == enum.Candle.RED:
            if highPrice > prev_highPrice and closePrice < prev_lowPrice:
                result = mEnum.MarketType.BEARISH 

    return result

#open and close of the doji should fall within 10 percent
#for bulish doji, the high should be below the 10 sma. Also, one of two following bar must close above the high of doji
#for bearish doji, the low should be above the 10 sma. Also, one of two following bar must close below the low of doji
def findDojiReversalPattern(openPrice, highPrice, lowPrice, closePrice, prev_openPrice, prev_highPrice, prev_lowPrice, prev_closePrice, prev2_openPrice, prev2_highPrice, prev2_lowPrice, prev2_closePrice, avgPrevCandleSize, sma):
    prev_bodyWidth = candle.getWidth(prev_openPrice, prev_closePrice)
    prev_candleWidth = candle.getWidth(prev_highPrice, prev_lowPrice)

    bodyWidth = candle.getWidth(openPrice, closePrice)
    candleWidth = candle.getWidth(highPrice, lowPrice)

    diffWithPrev = mCom.PercentageBy_Solid(prev_candleWidth, avgPrevCandleSize)
    bodyPercent = mCom.FindDifferencePercentage(bodyWidth, candleWidth)
    #bobyPercentWithTail = candle.getBobyPercentWithTail(openPrice, highPrice, lowPrice, closePrice)   
    isPrev_Doji = candle.find_Doji(prev_openPrice, prev_highPrice, prev_lowPrice, prev_closePrice, 10)

    dojiMarketType = mEnum.MarketType.NONE
    if isPrev_Doji and diffWithPrev < 0:
        if prev_lowPrice > sma:
            dojiMarketType = mEnum.MarketType.BEARISH
        elif prev_highPrice < sma:
            dojiMarketType = mEnum.MarketType.BULLISH
    result = mEnum.MarketType.NONE
    if dojiMarketType != mEnum.MarketType.NONE:
        if dojiMarketType == mEnum.MarketType.BEARISH:
            if closePrice < prev_lowPrice:
                result = mEnum.MarketType.BEARISH
        elif dojiMarketType == mEnum.MarketType.BULLISH:
            if closePrice > prev_highPrice:
                result = mEnum.MarketType.BULLISH

    #check 2nd attempt - 2nd candle after doji
    if dojiMarketType == mEnum.MarketType.NONE:
        prev2_candleWidth = candle.getWidth(prev2_highPrice, prev2_lowPrice)
        isPrev2_Doji = candle.find_Doji(prev2_openPrice, prev2_highPrice, prev2_lowPrice, prev2_closePrice, 10)
        diffWithPrev = mCom.PercentageBy(prev2_candleWidth, avgPrevCandleSize)
        if isPrev2_Doji and diffWithPrev > 0:
            if prev2_lowPrice > sma:
                dojiMarketType = mEnum.MarketType.BEARISH
            elif prev2_highPrice < sma:
                dojiMarketType = mEnum.MarketType.BULLISH
        result = mEnum.MarketType.NONE
        if dojiMarketType != mEnum.MarketType.NONE:
            if dojiMarketType == mEnum.MarketType.BEARISH:
                if closePrice < prev2_lowPrice:
                    result = mEnum.MarketType.BEARISH
            elif dojiMarketType == mEnum.MarketType.BULLISH:
                if closePrice > prev2_highPrice:
                    result = mEnum.MarketType.BULLISH

    return result