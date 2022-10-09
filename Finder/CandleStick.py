import Enum.CommonEnum as enum

def getCandleColor(openPrice, ClosePrice):
    if openPrice < ClosePrice:
        candle = enum.Candle.GREEN
    elif openPrice > ClosePrice:
        candle = enum.Candle.RED
    else:
        # Equilibrium/Dojis candlestick
        candle = enum.Candle.NONE 
    return candle

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


    