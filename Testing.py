from datetime import datetime, timedelta
import json
import pandas as pd
import YahooAPI as yapi
import PivotPoint as pvpt
import CommonEnum as enum
import StockList as slidt
import os

def PlaceOrderBasedOnPivotPoint():
    trade_list = [] #empty list
    startdate = datetime.now() - timedelta(days=23)
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
                    if index.weekday() == 0:  
                        startdate1 = index - timedelta(days=3)
                    else:                    
                        startdate1 = index - timedelta(days=1)

                    stock1 = yapi.get_one_day_data(tickers=ticket, start=startdate1, interval="1d")
                    
                    #holiday finding
                    while not len(stock1) > 0:                   
                        startdate1 = startdate1 - timedelta(days=1)
                        stock1 = yapi.get_one_day_data(tickers=ticket, start=startdate1, interval="1d")
                    
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

                    stoplossrange = (r1-s1)/100 * 10  
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

                if live_open_price < live_close_price:
                    candle = enum.Candle.GREEN
                elif live_open_price > live_close_price:
                    candle = enum.Candle.RED
                else:
                    candle = enum.Candle.NONE 

                if (live_high_price >= r1 >= live_low_price) or (live_high_price >= r2 >= live_low_price) or (live_high_price >= r3 >= live_low_price) or (live_high_price >= r4 >= live_low_price):
                    in_line = enum.InLine.RESISTENCE
                elif (live_high_price >= s1 >= live_low_price) or (live_high_price >= s2 >= live_low_price) or (live_high_price >= s3 >= live_low_price) or (live_high_price >= s4 >= live_low_price):
                    in_line = enum.InLine.SUPPORT  
                else:
                    in_line = enum.InLine.NONE
               
                halfCandle = (prev_close_price+prev_open_price)/2
                if round(live_close_price, 2) > round(halfCandle , 2):
                    trend = enum.Trend.UP  
                elif round(live_close_price, 2) < round(halfCandle, 2):
                    trend = enum.Trend.DOWN  
                elif round(live_close_price, 2) == round(prev_close_price, 2):
                    trend = enum.Trend.STRAIGHT
                else:
                    trend = enum.Trend.NONE

                position = enum.Position.NONE
                if s1 <= live_close_price <= r1 or s1 <= live_open_price <= r1:
                    position = enum.Position.CPR
                    if position not in position_history:
                        position_history.append(position)
                if r2 >= live_close_price >= r1 or r2 >= live_open_price >= r1:
                    position = enum.Position.R12
                    if position not in position_history:
                        position_history.append(position)
                if r3 >= live_close_price >= r2 or r3 >= live_open_price >= r2:
                    position = enum.Position.R23
                    if position not in position_history:
                        position_history.append(position)
                if r4 >= live_close_price >= r3 or r4 >= live_open_price >= r3:
                    position = enum.Position.R34
                    if position not in position_history:
                        position_history.append(position)
                if s2 <= live_close_price <= s1 or s2 <= live_open_price <= s1:
                    position = enum.Position.S12
                    if position not in position_history:
                        position_history.append(position)
                if s3 <= live_close_price <= s2 or s3 <= live_open_price <= s2:
                    position = enum.Position.S23
                    if position not in position_history:
                        position_history.append(position)
                if s4 <= live_close_price <= s3 or s4 <= live_open_price <= s3:
                    position = enum.Position.S34
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

                prev_low_price = live_low_price
                prev_high_price = live_high_price
                prev_close_price = live_close_price
                prev_open_price = live_open_price

                if len(position_history) >= 2 and trend == enum.Trend.UP and trade == enum.Trade.NO:
                    if enum.Position.R12 == position and break_out_at == enum.BreakOut.RESISTENCE:
                        print("Buy at T1 " + str(live_close_price) + " at " + str(cur_time))
                        #Taking risk since it is in resistance level
                        riskcount = 1
                        enter_at = live_close_price
                        stop_loss_at = enter_at - (stoplossrange)
                        print("Stop Loss at " + str(stop_loss_at))
                        trade = enum.Trade.T1
                    elif (enum.Position.CPR in position_history or enum.Position.S12 in position_history) and support_breakout_count > 1: 
                        print("Buy at T2 " + str(live_close_price) + " at " + str(cur_time))
                        enter_at = live_close_price
                        stop_loss_at = enter_at - (stoplossrange)
                        print("Stop Loss at " + str(stop_loss_at))
                        trade = enum.Trade.T2
                    elif (enum.Position.R12 in position_history or enum.Position.R23 in position_history) and resistance_breakout_count > 0:
                        print("Buy at T3 " + str(live_close_price) + " at " + str(cur_time))
                        #Taking risk since it is in upper resistance level
                        riskcount = 1
                        enter_at = live_close_price
                        stop_loss_at = enter_at - (stoplossrange)
                        print("Stop Loss at " + str(stop_loss_at))
                        trade = enum.Trade.T3

                if enter_at != 0:
                    profit_price = 0
                    if trade == enum.Trade.T1:
                        if resistance_breakout_count > 1:
                            profit_price = live_close_price - enter_at
                            profit = (profit_price / live_close_price) * 100
                            print("Sell at T1 " + str(live_close_price) + " at " + str(cur_time))  
                            print("Profit at = " + str(profit) + " at " + str(cur_time))
                            enter_at = 0 
                            riskcount = 0
                            # if profit > 0, then special monitor case to exist
                                
                        if riskcount > 0:
                            print("Taking Risk T1 at = " + str(cur_time))  
                            riskcount = riskcount - 1
                    elif trade == enum.Trade.T2:
                        if resistance_breakout_count > 0:
                            profit_price = live_close_price - enter_at
                            profit = (profit_price / live_close_price) * 100
                            print("Sell at T2 " + str(live_close_price) + " at " + str(cur_time))  
                            print("Profit at = " + str(profit) + " at " + str(cur_time))
                            enter_at = 0 
                            # if profit > 0, then special monitor case to exist 
                    elif trade == enum.Trade.T3:
                        if resistance_breakout_count > 1 and enum.Position.R23 in position_history:
                            profit_price = live_close_price - enter_at
                            profit = (profit_price / live_close_price) * 100

                            #Taking risk since it is in upper resistance level
                            if profit > 0 or riskcount == 0:                           
                                print("Sell at T3 " + str(live_close_price) + " at " + str(cur_time))  
                                print("Profit at = " + str(profit) + " at " + str(cur_time))  
                                enter_at = 0
                                riskcount = 0
                                # if profit > 0, then special monitor case to exist
                                
                            if riskcount > 0:
                                print("Taking Risk T3 at = " + str(cur_time))  
                                riskcount = riskcount - 1
                    totalprofit = totalprofit + profit_price

                if enter_at != 0:
                    if stop_loss_at >= live_close_price and riskcount == 0:
                        # wait since still it is in resistance line
                        if in_line == enum.InLine.RESISTENCE and (trade == enum.Trade.T1 or trade == enum.Trade.T3):
                            continue
                        profit_price = live_close_price - enter_at
                        profit = (profit_price / live_close_price) * 100
                        print("Stop Less Hit at price " + str(live_close_price) + " at " + str(cur_time))  
                        print("Profit at = " + str(profit) + " at " + str(cur_time))  
                        enter_at = 0
                    if str(cur_time) == "15:25":
                        profit_price = live_close_price - enter_at
                        profit = (profit_price / live_close_price) * 100
                        print("Market Closed at price " + str(live_close_price) + " at " + str(cur_time))  
                        print("Profit at = " + str(profit) + " at " + str(cur_time))  
                        enter_at = 0 
                    totalprofit = totalprofit + profit_price

            new_dict = slidt.constructorderjson(rows, stock['close'][len(stock)-1])                  
            trade_list.append(new_dict)

    print("Total Profit = " + str(totalprofit))            
    return trade_list

PlaceOrderBasedOnPivotPoint()
