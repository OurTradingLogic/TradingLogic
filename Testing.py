from datetime import datetime, timedelta
import json
import pandas as pd
import Utility.YahooAPI as yapi
import Finder.PivotPoint as pvpt
import Enum.CommonEnum as enum
import Helper.StockList as slidt
import Finder.CandleStick as candl
import Finder.SupportResistence as sr
import Finder.RiskManagement as rmanage
import Finder.Trade as trading
import os

def PlaceOrderBasedOnPivotPoint():
    trade_list = [] #empty list
    startdate = datetime.now() - timedelta(days=30)
    enddate = datetime.now()

    alllist = slidt.getfrompivotpointexcel() 
    
    inte = 1
    intetotal = 0
    totalprofit = 0
    for rows in alllist:
        if inte > 11:
            os.system('clear')
            inte = 0

        print(str(intetotal))
        inte = inte + 1
        intetotal = intetotal +1
        ticket = str(rows['tradingsymbol'])
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

        stock = yapi.get_historic_data(tickers=ticket, start=startdate, end=enddate, interval="5m")
        if len(stock) > 0:
            stock = stock.set_index('date')
            for index, row in stock.iterrows():
                cur_date = index.strftime('%d/%m/%Y')
                cur_time = index.strftime("%H:%M")
                if prev_date != cur_date:    

                    stock1 = yapi.get_one_day_data_skip_holiday(tickers=ticket, index=index)
                                        
                    print("************" + str(cur_date) + "***********************")
                    stock1 = stock1.set_index('date')

                    pvpt.get_cpr_pivots(stock1)

                    last = len(stock1)-1
                    cpr = stock1['Pivot'][last]
                    r1 = stock1['R1'][last]
                    s1 = stock1['S1'][last]
                    r2 = stock1['R2'][last]
                    s2 = stock1['S2'][last]
                    r3 = stock1['R3'][last]
                    s3 = stock1['S3'][last]
                    r4 = stock1['R4'][last]
                    s4 = stock1['S4'][last]

                    stoplossrange = rmanage.getstoplossrange(r1, s1)  
                    riskcount = 0                

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

                prev_date = cur_date

                live_close_price = row['close']
                live_low_price = row['low']
                live_high_price = row['high']
                live_open_price = row['open']

                candle = candl.getCandleColor(live_open_price, live_close_price)
                in_line = sr.findInLineSRPosition(live_low_price, live_high_price, r1, s1, r2, s2, r3, s3, r4, s4)              
                trend = candl.getTrend(prev_open_price, prev_close_price, live_close_price)
           
                position = sr.getPosition(live_open_price, live_close_price, r1, s1, r2, s2, r3, s3, r4, s4)             
                if position not in position_history:
                    position_history.append(position)                 
                
                #if position != enum.Position.NONE and position not in position_history:
                    #position_history.append(position)

                break_out_at = sr.findBreakOutPosition(candle, live_open_price, live_close_price, r1, s1, r2, s2, r3, s3, r4, s4)
                if break_out_at == enum.BreakOut.RESISTENCE:
                    resistance_breakout_count = resistance_breakout_count + 1
                    print("Found break out at " + str(enum.BreakOut.RESISTENCE) + ":" + str(live_close_price) + " at " + str(cur_time))
                elif break_out_at == enum.BreakOut.SUPPORT:
                    support_breakout_count = support_breakout_count + 1
                    print("Found break out at " + str(enum.BreakOut.SUPPORT) + ":" + str(live_close_price) + " at " + str(cur_time))

                prev_low_price = live_low_price
                prev_high_price = live_high_price
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

            new_dict = slidt.constructorderjson(rows, stock['close'][len(stock)-1])                  
            trade_list.append(new_dict)

    print("Total Profit = " + str(totalprofit * 50))            
    return trade_list

PlaceOrderBasedOnPivotPoint()
