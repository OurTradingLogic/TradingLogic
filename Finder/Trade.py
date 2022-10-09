import Enum.CommonEnum as enum
import Utility.Constant as cons

def Buy(stoplossrange, position_history, trend, position, break_out_at, resistance_breakout_count, support_breakout_count, live_close_price):
    riskcount = 0
    enter_at = 0
    stop_loss_at = 0
    trade = enum.Trade.NO
    if len(position_history) >= 2 and trend == enum.Trend.UP:
        if enum.Position.R12 == position and break_out_at == enum.BreakOut.RESISTENCE:
            #Taking risk since it is in resistance level
            riskcount = 1
            enter_at = live_close_price
            stop_loss_at = enter_at - (stoplossrange)
            trade = enum.Trade.T1
        elif (enum.Position.CPR in position_history or enum.Position.S12 in position_history) and support_breakout_count > 1: 
            enter_at = live_close_price
            stop_loss_at = enter_at - (stoplossrange)
            trade = enum.Trade.T2
        elif (enum.Position.R12 in position_history or enum.Position.R23 in position_history) and resistance_breakout_count > 0:
            #Taking risk since it is in upper resistance level
            riskcount = 1
            enter_at = live_close_price
            stop_loss_at = enter_at - (stoplossrange)
            trade = enum.Trade.T3
    return trade, riskcount, stop_loss_at, enter_at

def Sell(trade, riskcount, position_history, resistance_breakout_count, enter_at, live_close_price):
    executed = False
    riskTaken = False
    if enter_at != 0:
        profit_price = 0
        if trade == enum.Trade.T1:
            if resistance_breakout_count > 1:
                #profit_price = live_close_price - enter_at
                #profit = (profit_price / live_close_price) * 100
                executed = True
                # if profit > 0, then special monitor case to exist
                    
            if riskcount > 0:
                riskTaken = True
            
        elif trade == enum.Trade.T2:
            if resistance_breakout_count > 0:
                #profit_price = live_close_price - enter_at
                #profit = (profit_price / live_close_price) * 100
                executed = True
                # if profit > 0, then special monitor case to exist 

        elif trade == enum.Trade.T3:
            if resistance_breakout_count > 1 and enum.Position.R23 in position_history:
                profit_price = live_close_price - enter_at
                profit = (profit_price / live_close_price) * 100

                #Taking risk since it is in upper resistance level
                if profit > 0 or riskcount == 0:
                    executed = True
                    # if profit > 0, then special monitor case to exist
                    
                if riskcount > 0: 
                    riskTaken = True

    return executed, riskTaken

def SellStopLess(stop_loss_at, trade, riskcount, in_line, enter_at, live_close_price, cur_time):
    executed = False
    if enter_at != 0:
        if stop_loss_at >= live_close_price and riskcount == 0:
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