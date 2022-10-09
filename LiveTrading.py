import threading, time
#from yahoo_fin import stock_info as si
from datetime import datetime, timedelta
import json
import pandas as pd
import Utility.YahooAPI as yapi
import Finder.PivotPoint as pvpt
import Enum.CommonEnum as enum
import Helper.StockList as slidt
import os
import Utility.Constant as cons
import Finder.CandleStick as candl
import Finder.SupportResistence as sr
import Finder.RiskManagement as rmanage
import Finder.Trade as trading

ticket = 'ADANIPOWER'
cpr = 0 #str(rows['CPR'])
r1 = 0 #str(rows['R1'])
s1 = 0 #str(rows['S1'])
r2 = 0 #str(rows['R2'])
s2 = 0 #str(rows['S2'])
r3 = 0 #str(rows['R3'])
s3 = 0 #str(rows['S3'])
r4 = 0 #str(rows['R4'])
s4 = 0 #str(rows['R4'])
stoplossrange = 0

cur_date = 0
prev_date = 0
cur_time = 0
live_low_price = 0
prev_low_price = 0
live_high_price = 0
prev_high_price = 0
live_close_price = 0
prev_close_price = 0
live_open_price = 0
prev_open_price = 0
support_breakout_count = 0
resistance_breakout_count = 0

enter_at = 0
stop_loss_at = 0

position_history = []

in_line = enum.InLine.NONE
trend = enum.Trend.NONE
position = enum.Position.NONE
break_out_at = enum.BreakOut.NONE
candle = enum.Candle.NONE
trade = enum.Trade.NO

riskcount = 0
totalprofit = 0
live_price = 0

lastdate = datetime.now() - timedelta(days=1)
stock = yapi.get_one_day_valid_data(tickers=ticket, start=lastdate)

stock = stock.set_index('date')
pvpt.get_cpr_pivots(stock)

last = len(stock)-1
cpr = stock['Pivot'][last]
r1 = stock['R1'][last]
s1 = stock['S1'][last]
r2 = stock['R2'][last]
s2 = stock['S2'][last]
r3 = stock['R3'][last]
s3 = stock['S3'][last]
r4 = stock['R4'][last]
s4 = stock['S4'][last]

stoplossrange = rmanage.getstoplossrange(r1, s1)
riskcount = 0   
inte = 0
print("Pivot Points " + str(r1) + " " + str(s1))
ticker = threading.Event()
while not ticker.wait(cons.WAIT_TIME_SECONDS):
    if inte > 300:
        os.system('clear')
        inte = 0
    inte = inte + 1

    cur_time = datetime.now().strftime("%H:%M:%S")
    cur_minute = datetime.now().strftime("%M")
    
    try:
        live_close_price = yapi.get_live_price(ticket)
    except:
        live_close_price = prev_close_price
        print("Exception")

    if live_open_price == 0:
        live_open_price = live_close_price
    if live_high_price <=  live_close_price:
        live_high_price = live_close_price
    elif live_low_price >=  live_close_price:
        live_low_price = live_close_price
    print("Tick (Wait for collecting data) at " + str(cur_time) + " Live Price = " + str(live_close_price))
        
    if cur_minute.endswith('5') or cur_minute.endswith('0'):
        cur_time = datetime.now().strftime("%H:%M:%S")
        print("Trying for perform with data at " + str(cur_time))
        
        candle = candl.getCandleColor(live_open_price, live_close_price)
        in_line = sr.findInLineSRPosition(live_low_price, live_high_price, r1, s1, r2, s2, r3, s3, r4, s4)
        trend = candl.getTrend(prev_open_price, prev_close_price, live_close_price)

        position = sr.getPosition(live_open_price, live_close_price, r1, s1, r2, s2, r3, s3, r4, s4)             
        if position not in position_history:
            position_history.append(position)                 
        
        #if position != enum.Position.NONE and position not in position_history:
            #position_history.append(position)

        if candle == enum.Candle.GREEN and (live_close_price >= r1 >= live_open_price or live_close_price >= r2 >= live_open_price or live_close_price >= r3 >= live_open_price or live_close_price >= r4 >= live_open_price):
            break_out_at = enum.BreakOut.RESISTENCE
            resistance_breakout_count = resistance_breakout_count + 1
            print("Found break out at " + str(enum.BreakOut.RESISTENCE) + ":" + str(live_close_price) + " at " + str(cur_time))
        elif candle == enum.Candle.RED and (live_close_price <= s1 <= live_open_price or live_close_price <= s2 <= live_open_price or live_close_price <= s3 <= live_open_price or live_close_price <= s4 <= live_open_price):
            break_out_at = enum.BreakOut.SUPPORT
            support_breakout_count = support_breakout_count + 1
            print("Found break out at " + str(enum.BreakOut.SUPPORT) + ":" + str(live_close_price) + " at " + str(cur_time))    

        prev_close_price = live_close_price
        prev_open_price = live_open_price

        if trade == enum.Trade.NO:
            trade, riskcount, stop_loss_at, enter_at = trading.Buy(stoplossrange, position_history, trend, position, break_out_at, resistance_breakout_count, support_breakout_count, live_close_price)
            if trade != enum.Trade.NO:    
                print("Buy " + str(trade) + " at price " + str(live_close_price) + " on " + str(cur_time))
                print("Stop Loss at " + str(stop_loss_at))

        if enter_at != 0:
            profit_price = 0
            executed, riskTaken = trading.Sell(trade, riskcount, position_history, resistance_breakout_count, enter_at, live_close_price)
            if executed:
                profit_price = live_close_price - enter_at
                profit = (profit_price / live_close_price) * 100  
                print("Sell " + str(trade) + " at price " + str(live_close_price) + " on " + str(cur_time))  
                print("Profit at = " + str(profit) + " at " + str(cur_time))
                enter_at = 0 
                riskcount = 0
            if riskTaken:
                print("Taking Risk at = " + str(cur_time)) 
                riskcount = riskcount - 1

            totalprofit = totalprofit + profit_price

        if enter_at != 0:
            profit_price = 0
            executed = trading.SellStopLess(stop_loss_at, trade, riskcount, in_line, enter_at, live_close_price, cur_time)
            if executed:
                profit_price = live_close_price - enter_at
                profit = (profit_price / live_close_price) * 100
                enter_at = 0    
                print("Stop Less Hit at price " + str(live_close_price) + " at " + str(cur_time))  
                print("Profit at = " + str(profit) + " at " + str(cur_time))  

            if profit_price > 0:
                totalprofit = totalprofit + profit_price

print("Total Profit = " + str(totalprofit))
print("Trade on " + str(trade))