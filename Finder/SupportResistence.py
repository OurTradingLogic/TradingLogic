import Enum.CommonEnum as enum

def findInLineSRPosition(live_low_price, live_high_price, r1, s1, r2, s2, r3, s3, r4, s4):
    if (live_high_price >= r1 >= live_low_price) or (live_high_price >= r2 >= live_low_price) or (live_high_price >= r3 >= live_low_price) or (live_high_price >= r4 >= live_low_price):
        in_line = enum.InLine.RESISTENCE
    elif (live_high_price >= s1 >= live_low_price) or (live_high_price >= s2 >= live_low_price) or (live_high_price >= s3 >= live_low_price) or (live_high_price >= s4 >= live_low_price):
        in_line = enum.InLine.SUPPORT  
    else:
        in_line = enum.InLine.NONE
    return in_line

def getPosition(live_open_price, live_close_price, r1, s1, r2, s2, r3, s3, r4, s4):
    position = enum.Position.NONE
    if s1 <= live_close_price <= r1 or s1 <= live_open_price <= r1:
        position = enum.Position.CPR
    elif r2 >= live_close_price >= r1 or r2 >= live_open_price >= r1:
        position = enum.Position.R12
    elif r3 >= live_close_price >= r2 or r3 >= live_open_price >= r2:
        position = enum.Position.R23
    elif r4 >= live_close_price >= r3 or r4 >= live_open_price >= r3:
        position = enum.Position.R34
    elif s2 <= live_close_price <= s1 or s2 <= live_open_price <= s1:
        position = enum.Position.S12
    elif s3 <= live_close_price <= s2 or s3 <= live_open_price <= s2:
        position = enum.Position.S23
    elif s4 <= live_close_price <= s3 or s4 <= live_open_price <= s3:
        position = enum.Position.S34 
    return position

def findBreakOutPosition(candle, live_open_price, live_close_price, r1, s1, r2, s2, r3, s3, r4, s4):
    break_out_at = enum.BreakOut.NONE
    if candle == enum.Candle.GREEN and (live_close_price >= r1 >= live_open_price or live_close_price >= r2 >= live_open_price or live_close_price >= r3 >= live_open_price or live_close_price >= r4 >= live_open_price):
        break_out_at = enum.BreakOut.RESISTENCE
    elif candle == enum.Candle.RED and (live_close_price <= s1 <= live_open_price or live_close_price <= s2 <= live_open_price or live_close_price <= s3 <= live_open_price or live_close_price <= s4 <= live_open_price):
        break_out_at = enum.BreakOut.SUPPORT
    return break_out_at
