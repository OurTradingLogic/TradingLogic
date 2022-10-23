from cgitb import reset
import Enum.CommonEnum as enum

def getCandleColor(openPrice, closePrice):
    if openPrice < closePrice:
        candle = enum.Candle.GREEN
    elif openPrice > closePrice:
        candle = enum.Candle.RED
    else:
        # Equilibrium/Dojis candlestick
        candle = enum.Candle.BLACK 
    return candle
    
def isGreen(openPrice, closePrice):
    return openPrice < closePrice

def isRed(openPrice, closePrice):
    return openPrice > closePrice

def getWidth(openPrice, closePrice):
    return abs(closePrice-openPrice)

def getLowerTailWidth(openPrice, lowPrice, closePrice):
    if isGreen(openPrice, closePrice):
        return abs(lowPrice-openPrice)
    else: return abs(lowPrice-closePrice)

def getUpperTailWidth(openPrice, highPrice, closePrice):
    if isGreen(openPrice, closePrice):
        return abs(highPrice-closePrice)
    else: return abs(highPrice-openPrice)

def getTrend(prev_open_price, prev_close_price, live_close_price):
    halfCandle = (prev_close_price+prev_open_price)/2
    if round(live_close_price, 2) > round(halfCandle , 2):
        trend = enum.Trend.UP  
    elif round(live_close_price, 2) < round(halfCandle, 2):
        trend = enum.Trend.DOWN  
    elif round(live_close_price, 2) == round(prev_close_price, 2):
        trend = enum.Trend.STRAIGHT
    else:
        trend = enum.Trend.NONE
    return trend

def isBigRedCandle(openPrice, highPrice, lowPrice, closePrice):
    body = getWidth(openPrice, closePrice)
    lower_tail = getLowerTailWidth(openPrice, lowPrice, closePrice)
    upper_tail = getUpperTailWidth(openPrice, highPrice, closePrice)
    tail = lower_tail + upper_tail
    if body > tail * 10:
        return True
    else:
        return False

def find_Hammer_Sys(openPrice, highPrice, lowPrice, closePrice):
    body = getWidth(openPrice, closePrice)
    lower_tail = getLowerTailWidth(openPrice, lowPrice, closePrice)
    upper_tail = getUpperTailWidth(openPrice, highPrice, closePrice)
    wick = body * 2
    hammer = enum.HammerCandleSys.NONE
    if closePrice > openPrice: 
        if lower_tail > wick and highPrice == closePrice:
            hammer = enum.HammerCandleSys.Hammer
        #elif (Close-Open) < body and  (Low-Open) > wick and (High == Open)   
        elif lower_tail > wick and lowPrice == openPrice:
            hammer = enum.HammerCandleSys.InvertedHammer
    elif closePrice < openPrice: 
        if upper_tail > wick and highPrice == openPrice: 
            hammer = enum.HammerCandleSys.HangingMan
        #elif closePrice < openPrice and upper_tail > wick and lowPrice == openPrice: 
        elif upper_tail > wick and lowPrice == closePrice: 
            hammer = enum.HammerCandleSys.ShootingStar
    return hammer

def find_Star_Sys(openPrice, highPrice, closePrice, prev1_openPrice, prev1_highPrice, prev1_lowPrice, prev1_closePrice, prev2_openPrice, prev2_closePrice):
    result = enum.StarCandleSys.NONE
    prev2_body = getWidth(prev2_openPrice, prev2_closePrice)
    cur_boby = getWidth(openPrice, closePrice)
    min_side_body = min(prev2_body, cur_boby)
    middle_body = getWidth(prev1_openPrice, prev1_closePrice)
    lower_middle_tail = getLowerTailWidth(prev1_openPrice, prev1_lowPrice, prev1_closePrice)
    upper_middle_tail = getUpperTailWidth(prev1_openPrice, prev1_highPrice, prev1_closePrice)

    isStarCandleEligible = (lower_middle_tail >= middle_body) and (upper_middle_tail >= middle_body)
    if not isStarCandleEligible:
        if isGreen(openPrice, closePrice) and openPrice < prev1_closePrice and \
            isGreen(prev1_openPrice, prev1_closePrice) and  prev1_closePrice < prev2_closePrice and \
            isRed(prev2_openPrice, prev2_closePrice) and \
            prev2_body > min_side_body and (highPrice-openPrice)>min_side_body:
            result = enum.StarCandleSys.MORNING
        elif isRed(openPrice, closePrice) and openPrice > prev1_closePrice and \
                isRed(prev1_openPrice, prev1_closePrice) and  prev1_closePrice > prev2_closePrice and \
                isGreen(prev2_openPrice, prev2_closePrice) and \
                prev2_body > min_side_body and (highPrice-closePrice)>min_side_body:
            result = enum.StarCandleSys.EVENING

    return result

def find_Doji_Sys(openPrice, closePrice, prev_openPrice, prev_closePrice):
    result = enum.DojiCandleSys.NONE
    # Bullish Doji    
    if isRed(prev_openPrice, prev_closePrice) and closePrice == openPrice:
        result = enum.DojiCandleSys.BULL
    # Bearish Doji     
    elif isGreen(prev_openPrice, prev_closePrice) and closePrice == openPrice:
        result = enum.DojiCandleSys.BEAR
    return result

def find_Marubozu_Sys(openPrice, highPrice, lowPrice, closePrice):
    result = enum.MarubozuCandleSys.NONE
    # Bullish Marubozu      
    if isGreen(openPrice, closePrice) and \
        closePrice == highPrice and \
        openPrice == lowPrice:
         result = enum.MarubozuCandleSys.BULL
    # Bearish Marubozu      
    if isRed(openPrice, closePrice) and \
        closePrice == lowPrice and \
        openPrice == highPrice:
         result = enum.MarubozuCandleSys.BULL 
    return result