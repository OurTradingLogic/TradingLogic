from cgitb import reset
import Enum.CommonEnum as enum
import Utility.Constant as cons
from datetime import datetime, timedelta
import Finder.CandleStick as candl
import Finder.SupportResistence as sr
import Finder.Signal as signal

def checkIgnore(cur_time, live_high_price, live_low_price, live_close_price, first_resistence_at, first_support_at, r1, s1, r2, s2, r3, s3, r4, s4, first_candle):
    result = False

    if datetime.strptime(cur_time, '%H:%M').time() > datetime.strptime('10:00', '%H:%M').time() and (first_resistence_at == 0 or first_support_at == 0):
        result = True
    elif live_close_price < s3:
        result = True
    elif first_candle != enum.Signal.BUY:
        result = True
    #elif cur_time == cons.MARKET_START_TIME:
        #inline = sr.findInLineSRPosition(live_low_price, live_high_price, r1, s1, r2, s2, r3, s3, r4, s4) 
       # if inline != enum.InLine.NONE:
            #result = True

    return result

def Enter(cur_time, stoplossrange, position_history, trend, position, break_out_at, resistance_breakout_count, support_breakout_count, first_support_breakout_count, first_resistence_at, first_support_at, live_open_price, live_high_price, live_low_price, live_close_price, r1, s1, r2, s2, r3, s3, r4, s4, alert, first_candle):
    riskcount = 0
    enter_at = 0
    stop_loss_at = 0
    trade = enum.Trade.NO  
    ignore = checkIgnore(cur_time, live_high_price, live_low_price, live_close_price, first_resistence_at, first_support_at, r1, s1, r2, s2, r3, s3, r4, s4, first_candle)
    candle = candl.getCandleColor(live_open_price, live_close_price)
    if not ignore:
        if len(position_history) > 0 and trend == enum.Trend.UP:
            if enum.Position.R12 == position and enum.Position.CPR == position and break_out_at == enum.BreakOut.RESISTENCE:
                #Taking risk since it is in resistance level
                riskcount = 1
                enter_at = live_close_price
                stop_loss_at = live_open_price - (stoplossrange)
                trade = enum.Trade.T1
            elif (enum.Position.CPR in position_history or enum.Position.S12 in position_history) and support_breakout_count > 1:
            #elif (enum.Position.CPR in position_history or enum.Position.S12 in position_history) and support_breakout_count > 1 and findSupportAt < s1:
                enter_at = live_close_price
                stop_loss_at = enter_at - (stoplossrange)
                trade = enum.Trade.T2
            elif (enum.Position.R12 in position_history or enum.Position.R23 in position_history) and resistance_breakout_count > 0 and\
                 (break_out_at == enum.BreakOut.NONE or alert == enum.Alert.NONE) and live_close_price > r1:
                #Taking risk since it is in upper resistance level
                riskcount = 1
                enter_at = live_close_price
                stop_loss_at = enter_at - (stoplossrange)
                trade = enum.Trade.T3
        elif len(position_history) > 0 and trend == enum.Trend.DOWN:
            if enum.Position.CPR == position and first_support_breakout_count > 2 and live_high_price < first_support_at and candle == enum.Candle.RED:
                enter_at = live_close_price
                stop_loss_at = enter_at + (stoplossrange)
                trade = enum.Trade.S1            

    return trade, riskcount, stop_loss_at, enter_at

def Exit(trade, trend, riskcount, position_history, resistance_breakout_count, support_breakout_count, first_resistance_breakout_count,enter_at, live_open_price, live_high_price, live_low_price, live_close_price, prev_open_price, prev_close_price, r1, s1, r2, s2, r3, s3, r4, s4):
    executed = False
    riskTaken = False
    if enter_at != 0:
        profit_price = 0
        if trade == enum.Trade.T1:
            if resistance_breakout_count > 1 and trend == enum.Trend.DOWN:
                #profit_price = live_close_price - enter_at
                #profit = (profit_price / live_close_price) * 100
                executed = True
                # if profit > 0, then special monitor case to exist
                    
            if riskcount > 0:
                riskTaken = True
            
        elif trade == enum.Trade.T2:
            if resistance_breakout_count > 0 or (first_resistance_breakout_count > 1 and trend == enum.Trend.DOWN):
                #profit_price = live_close_price - enter_at
                #profit = (profit_price / live_close_price) * 100
                executed = True
                # if profit > 0, then special monitor case to exist 

        elif trade == enum.Trade.T3:
            in_linePP = sr.findInLinePivotPointPosition(live_low_price, live_high_price, r1, s1, r2, s2, r3, s3, r4, s4)
            if resistance_breakout_count > 1 and enum.Position.R23 in position_history:
                profit_price = live_close_price - enter_at
                profit = (profit_price / live_close_price) * 100

                #Taking risk since it is in upper resistance level
                if profit > 0 or riskcount == 0:
                    executed = True
                    # if profit > 0, then special monitor case to exist
                    
                if riskcount > 0: 
                    riskTaken = True
        elif trade == enum.Trade.S1:
            #if enum.Position.CPR in position_history and ((support_breakout_count > 1  and enum.Position.S12 in position_history) or \
                #candl.find_Doji_Sys(live_open_price, live_close_price, prev_open_price, prev_close_price)):
            if enum.Position.CPR in position_history and support_breakout_count > 1  and enum.Position.S12 in position_history:
                executed = True
    return executed, riskTaken

def SellStopLess(cur_time, stop_loss_at, trade, riskcount, in_line, enter_at, live_open_price, live_high_price, live_low_price, live_close_price):
    executed = False
    if enter_at != 0:
        if trade == enum.Trade.S1:
            if stop_loss_at <= live_close_price and riskcount == 0 and live_low_price > enter_at:
                executed = True
        elif stop_loss_at >= live_close_price and riskcount == 0 and live_high_price < enter_at:
            # wait since still it is in resistance line
            if not (in_line == enum.InLine.RESISTENCE and (trade == enum.Trade.T1 or trade == enum.Trade.T3)):
                executed = True
            #profit_price = live_close_price - enter_at
            #profit = (profit_price / live_close_price) * 100
        if str(cur_time) == cons.MARKET_END_TIME:
            #profit_price = live_close_price - enter_at
            #profit = (profit_price / live_close_price) * 100
            executed = True
    return executed

def ProfitCalc(trade, enter_at, exit_at):
    profit_price = 0
    profit = 0
    if trade == enum.Trade.S1:
        if False: #need to work on it
            profit_price = enter_at - exit_at
            profit = (profit_price / enter_at) * 100
    else:
        profit_price = exit_at - enter_at
        profit = (profit_price / exit_at) * 100
    return profit_price, profit


class Alert(object):
    alert = enum.Alert.NONE
    firstCandle = enum.Candle.BLACK

    def __del__(self):
        self.alert = enum.Alert.NONE
        self.firstCandle = enum.Candle.BLACK

    def Process(self, cur_time, live_open_price, live_high_price, live_low_price, live_close_price):
        if candl.isBigRedCandle(live_open_price, live_high_price, live_low_price, live_close_price):
            self.alert = enum.Alert.SHORTFALL
        if cur_time == cons.MARKET_START_TIME:
            self.firstCandle = signal.basedOnCandle(live_open_price, live_close_price)
