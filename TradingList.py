from datetime import datetime, timedelta
import json
import pandas as pd
import YahooAPI as yapi
import BollingerBand as bband
import PivotPoint as pvpt
import CommonEnum as enum
import StockList as slidt
import os

def gettradinglist2(source):
    trade_list = [] #empty list
    startdate = datetime.now() - timedelta(days=500)
    enddate = datetime.now()

    #percent = 0
    #amount = 0
    #stockcnt = 0
    #stockscnt = 0
    #total_percent = 0
    #total_amount = 0

    alllist = slidt.getlistfrom(source) 

    stocks = yapi.get_historic_data2(tickers=alllist, start=startdate, end=enddate, interval="1wk")
    for stock in stocks:
        if len(stock) > 0:
            #stock = stock.set_index('date')

            stock['sma_20'] = bband.sma(stock['close'], 20)
            stock['upper_bb'], stock['lower_bb'] = bband.bb(stock['close'], stock['sma_20'], 20)
            bband.break_out(stock)

            buy_price, sell_price, bb_signal, buy_date, sell_date = bband.implement_bb_strategy(stock, 1)

            #percent, amount, stockcnt = bband.calculateProfit(buy_price, sell_price, bb_signal, stock, ticket)
            #total_percent = total_percent + percent
            #stockscnt = stockscnt + stockcnt
            #total_amount = total_amount + amount

            if len(buy_date) > 0: 
                temp_last_buy_date = buy_date[len(buy_date)-1]
                #last_buy_date = datetime.strptime(temp_last_buy_date, "%Y-%m-%d")
                #last_buy_date = datetime.now().strftime("%Y-%m-%d")
                last_buy_date = temp_last_buy_date.strftime("%Y-%m-%d")
                temp_date = datetime.now() - timedelta(days=90)
                today_date = temp_date.strftime("%Y-%m-%d")
                #today_date = datetime.strptime((datetime.now() - timedelta(days=116)), "%d%m%y")
                
                if last_buy_date > today_date: 
                    row = alllist.loc[alllist['tradingsymbol'] == ""]
                    new_dict = slidt.constructorderjson(row, stock['close'][len(stock)-1])                  
                    trade_list.append(new_dict)
                    #print(buy_date)
                    #print(new_dict)

def gettradinglist(source):
    trade_list = [] #empty list
    startdate = datetime.now() - timedelta(days=500)
    enddate = datetime.now()

    #percent = 0
    #amount = 0
    #stockcnt = 0
    #stockscnt = 0
    #total_percent = 0
    #total_amount = 0

    alllist = slidt.getlistfrom(source) 
    inte = 1
    intetotal = 0
    for rows in alllist:
        if inte > 11:
            os.system('clear')
            inte = 0

        print(str(intetotal))
        inte = inte + 1
        intetotal = intetotal +1
        ticket = str(rows['tradingsymbol'])

        stock = yapi.get_historic_data(tickers=ticket, start=startdate, end=enddate, interval="1wk")
        if len(stock) > 0:
            stock = stock.set_index('date')

            stock['sma_20'] = bband.sma(stock['close'], 20)
            stock['upper_bb'], stock['lower_bb'] = bband.bb(stock['close'], stock['sma_20'], 20)
            bband.break_out(stock)

            buy_price, sell_price, bb_signal, buy_date, sell_date = bband.implement_bb_strategy(stock, 1)

            #percent, amount, stockcnt = bband.calculateProfit(buy_price, sell_price, bb_signal, stock, ticket)
            #total_percent = total_percent + percent
            #stockscnt = stockscnt + stockcnt
            #total_amount = total_amount + amount

            if len(buy_date) > 0: 
                temp_last_buy_date = buy_date[len(buy_date)-1]
                #last_buy_date = datetime.strptime(temp_last_buy_date, "%Y-%m-%d")
                #last_buy_date = datetime.now().strftime("%Y-%m-%d")
                last_buy_date = temp_last_buy_date.strftime("%Y-%m-%d")
                temp_date = datetime.now() - timedelta(days=30)
                today_date = temp_date.strftime("%Y-%m-%d")
                #today_date = datetime.strptime((datetime.now() - timedelta(days=116)), "%d%m%y")
                
                if last_buy_date > today_date: 
                    new_dict = slidt.constructorderjson(rows, stock['close'][len(stock)-1])                  
                    trade_list.append(new_dict)
                    #print(buy_date)
                    #print(new_dict)
    return trade_list

def getpivotpointtradinglist(source):
    trade_list = [] #empty list

    alllist = slidt.getfromjsondata(source) 
    inte = 1
    intetotal = 0
    for rows in alllist:
        if inte > 11:
            os.system('clear')
            inte = 0

        print(str(intetotal))
        inte = inte + 1
        intetotal = intetotal +1
        ticket = str(rows['tradingsymbol'])

        stock = yapi.get_last_day_data(tickers=ticket)
        if len(stock) > 0:
            stock = stock.set_index('date')

            pvpt.get_cpr_pivots(stock)

            last = len(stock)-1
            new_dict = slidt.constructpivotpointjson(rows, stock['Pivot'][last], stock['R1'][last], stock['S1'][last], stock['R2'][last],
            stock['S2'][last], stock['R3'][last], stock['S3'][last], stock['R4'][last], stock['S4'][last])                  
            trade_list.append(new_dict)
    return trade_list