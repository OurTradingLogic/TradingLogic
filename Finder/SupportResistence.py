import Enum.CommonEnum as enum
import Utility.Constant as cons

def findInLineSRPosition(live_low_price, live_high_price, r1, s1, r2, s2, r3, s3, r4, s4):
    if (live_high_price >= r1 >= live_low_price) or (live_high_price >= r2 >= live_low_price) or (live_high_price >= r3 >= live_low_price) or (live_high_price >= r4 >= live_low_price):
        in_line = enum.InLine.RESISTENCE
    elif (live_high_price >= s1 >= live_low_price) or (live_high_price >= s2 >= live_low_price) or (live_high_price >= s3 >= live_low_price) or (live_high_price >= s4 >= live_low_price):
        in_line = enum.InLine.SUPPORT  
    else:
        in_line = enum.InLine.NONE
    return in_line

def findInLinePivotPointPosition(live_low_price, live_high_price, r1, s1, r2, s2, r3, s3, r4, s4):
    if (live_high_price >= r1 >= live_low_price):
        in_line = enum.InLineSR.R1
    if (live_high_price >= r2 >= live_low_price):
        in_line = enum.InLineSR.R2
    if (live_high_price >= r3 >= live_low_price): 
        in_line = enum.InLineSR.R3
    if (live_high_price >= r4 >= live_low_price):
        in_line = enum.InLineSR.R4
    elif (live_high_price >= s1 >= live_low_price): 
        in_line = enum.InLineSR.S1
    if (live_high_price >= s2 >= live_low_price): 
        in_line = enum.InLineSR.S2
    if (live_high_price >= s3 >= live_low_price): 
        in_line = enum.InLineSR.S3
    if (live_high_price >= s4 >= live_low_price):
        in_line = enum.InLineSR.S4
    else:
        in_line = enum.InLineSR.NONE
    return in_line

def getPosition(live_open_price, live_close_price, r1, s1, r2, s2, r3, s3, r4, s4):
    position = enum.Position.NONE
    if s1 < live_close_price < r1 or s1 < live_open_price < r1:
        position = enum.Position.CPR
    elif r2 > live_close_price > r1 or r2 > live_open_price > r1:
        position = enum.Position.R12
    elif r3 > live_close_price > r2 or r3 > live_open_price > r2:
        position = enum.Position.R23
    elif r4 > live_close_price > r3 or r4 > live_open_price > r3:
        position = enum.Position.R34
    elif s2 < live_close_price < s1 or s2 < live_open_price < s1:
        position = enum.Position.S12
    elif s3 < live_close_price < s2 or s3 < live_open_price < s2:
        position = enum.Position.S23
    elif s4 < live_close_price < s3 or s4 < live_open_price < s3:
        position = enum.Position.S34 
    return position

def findBreakOutPosition(candle, live_open_price, live_high_price, live_low_price, live_close_price, r1, s1, r2, s2, r3, s3, r4, s4):
    break_out_at = enum.BreakOut.NONE
    if (candle == enum.Candle.GREEN) and (live_close_price >= r1 >= live_open_price or live_close_price >= r2 >= live_open_price or live_close_price >= r3 >= live_open_price or live_close_price >= r4 >= live_open_price):
        break_out_at = enum.BreakOut.RESISTENCE
    elif (candle == enum.Candle.RED) and (live_close_price <= s1 <= live_open_price or live_close_price <= s2 <= live_open_price or live_close_price <= s3 <= live_open_price or live_close_price <= s4 <= live_open_price):
        break_out_at = enum.BreakOut.SUPPORT
    elif (candle == enum.Candle.BLACK):
        if (live_high_price >= r1 >= live_low_price or live_high_price >= r2 >= live_low_price or live_high_price >= r3 >= live_low_price or live_high_price >= r4 >= live_low_price):
            break_out_at = enum.BreakOut.RESISTENCE
        elif (live_high_price >= s1 >= live_low_price or live_high_price >= s2 >= live_low_price or live_high_price >= s3 >= live_low_price or live_high_price >= s4 >= live_low_price):
            break_out_at = enum.BreakOut.SUPPORT

    return break_out_at

class SupportResistence(object):
    support_at = 0
    resistence_at = 0
    max_high_price = 0
    max_low_price = 0
    support_break_out_count = 0
    resistence_break_out_count = 0
    break_out_at = enum.BreakOut.NONE
    in_line = enum.InLine.NONE
    ab_line_formed = False
    ready_at_enter = enum.SR_First_Method.NONE
    ready_at_execute = enum.SR_First_Method.NONE
    #def __init__(self, time_start):
        #self.first_time_rs = time_start

    def __del__(self):
        self.support_at = 0
        self.resistence_at = 0
        self.max_high_price = 0
        self.max_low_price = 0
        self.support_break_out_count = 0
        self.resistence_break_out_count = 0
        self.break_out_at = enum.BreakOut.NONE
        self.in_line = enum.InLine.NONE
        self.ab_line_formed = False
        self.ready_at_enter = enum.SR_First_Method.NONE
        self.ready_at_execute = enum.SR_First_Method.NONE

    def process(self, cur_time, candle, trend, open_price, high_price, low_price, close_price):
        s_processed = False
        r_processed = False
        if self.resistence_at == 0:
            if cur_time <= cons.FIRST_TIME_RS:
                if candle == enum.Candle.GREEN:
                    if self.max_high_price !=0:
                        if self.max_high_price < high_price:
                            self.max_high_price = high_price
                    else:
                        self.max_high_price = high_price         
            else:
                self.resistence_at = self.max_high_price
                r_processed = True
        if self.support_at == 0:
            if cur_time <= cons.FIRST_TIME_RS:
                if candle == enum.Candle.RED:  
                    if self.max_low_price !=0: 
                        if self.max_low_price > low_price:
                            self.max_low_price = low_price
                    else:
                        self.max_low_price = low_price
            else:
                self.support_at = self.max_low_price
                s_processed = True
                
        break_out = self.findBreakOut(cur_time, candle, open_price, high_price, low_price, close_price)
        self.findInline(high_price, low_price)

        self.find_enter_at(candle, trend, open_price, close_price)
        self.find_execute_at(candle, trend, close_price)
        return s_processed, r_processed, break_out

    def findBreakOut(self, cur_time, candle, open_price, high_price, low_price, close_price):
        breakOut = False
        if (self.resistence_at != 0) and ((candle == enum.Candle.GREEN or cur_time == cons.MARKET_START_TIME) and close_price >= self.resistence_at >= open_price):
        #if (self.resistence_at != 0) and ((candle == enum.Candle.GREEN or cur_time == cons.MARKET_START_TIME) and high_price >= self.resistence_at >= low_price):
            self.break_out_at = enum.BreakOut.RESISTENCE
            self.resistence_break_out_count = self.resistence_break_out_count + 1
            breakOut = True
        elif (self.support_at != 0) and ((candle == enum.Candle.RED or cur_time == cons.MARKET_START_TIME) and close_price <= self.support_at <= open_price):
        #elif (self.support_at != 0) and ((candle == enum.Candle.RED or cur_time == cons.MARKET_START_TIME) and high_price >= self.support_at >= low_price):
            self.break_out_at = enum.BreakOut.SUPPORT
            self.support_break_out_count = self.support_break_out_count + 1
            breakOut = True
        elif cur_time == cons.MARKET_START_TIME:
            if (self.resistence_at != 0) and (high_price >= self.resistence_at >= low_price):
                self.break_out_at = enum.BreakOut.RESISTENCE
                self.resistence_break_out_count = self.resistence_break_out_count + 1
                breakOut = True
            elif (self.support_at != 0) and (high_price >= self.support_at >= low_price):
                self.break_out_at = enum.BreakOut.SUPPORT
                self.support_break_out_count = self.support_break_out_count + 1
                breakOut = True    
        return breakOut

    def findInline(self, high_price, low_price):
        if high_price >= self.resistence_at >= low_price:
            self.in_line = enum.InLine.RESISTENCE
        elif high_price >= self.support_at >= low_price:
            self.in_line = enum.InLine.SUPPORT
        else:
            self.in_line = enum.InLine.NONE
            self.ab_line_formed = True

    def find_enter_at(self, candle, trend, live_open_price, live_close_price):
        if self.break_out_at != enum.BreakOut.NONE:
            if self.ready_at_enter == enum.SR_First_Method.NONE and self.ab_line_formed:
                if self.break_out_at == enum.BreakOut.RESISTENCE:
                    if (trend == enum.Trend.UP or candle == enum.Candle.RED) and (live_close_price <= self.resistence_at <= live_open_price):
                        self.ready_at_enter = enum.SR_First_Method.BUY_AT_RESISTENCE
                elif self.break_out_at == enum.BreakOut.SUPPORT:
                    if (candle == enum.Candle.GREEN and live_close_price >= self.support_at >= live_open_price):
                        self.ready_at_enter = enum.SR_First_Method.BUY_AT_SUPPORT

    def find_execute_at(self, candle, trend, live_close_price):
        if self.ready_at_enter == enum.SR_First_Method.BUY_AT_RESISTENCE:
            if self.in_line != enum.InLine.RESISTENCE and candle == enum.Candle.RED and trend != enum.Trend.UP:
                self.ready_at_execute = enum.SR_First_Method.SELL
        elif self.ready_at_enter == enum.SR_First_Method.BUY_AT_SUPPORT:
            if self.in_line == enum.InLine.RESISTENCE or (candle == enum.Candle.RED and trend != enum.Trend.UP and self.in_line != enum.InLine.SUPPORT):
                self.ready_at_execute = enum.SR_First_Method.SELL


