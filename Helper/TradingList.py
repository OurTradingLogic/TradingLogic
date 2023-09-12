from datetime import datetime, timedelta
import json
import pandas as pd
import Utility.YahooAPI as yapi
import Finder.BollingerBand as bband
import Finder.PivotPoint as pvpt
import Enum.CommonEnum as enum
import Enum.IndicatorEnum as ienum
import Helper.StockList as slidt
import os
import Helper.JsonReader as jsonHelper
import Utility.GSheet as gsheet
import Helper.StockList as slist
import Finder.Indicators as tools
import Finder.Signal as snal
import Finder.PeekHighLow as peekHighLow
import sys

class TradingList:
    _importto = enum.ImportTo.NONE
    _wks = None
    def __init__(self, importto, exportFrom, isTest = False, jsonData = ""): 
        self._importto = importto
        self._indicator = tools.Indicator(jsonData)
        self._indicators = self._indicator.get()
        self._osignal = snal.Signal()
        self._isTest = isTest
        self._backTestFromDay = 0
        self._stockList = slist.StockList(exportFrom, isTest, jsonData).get()
        if importto == enum.ImportTo.GSHEET:
            if isTest:
                gSheetStockListConfig = jsonHelper.getnodedata('GSheet_TradingList_BackTesting')
                self._backTestFromDay = gSheetStockListConfig['fromday']
            else:
                gSheetStockListConfig = jsonHelper.getnodedata('GSheet_TradingList')
            gs = gsheet.GSheet(gSheetStockListConfig['File_Name'])
            self._wks = gs.sheet(gSheetStockListConfig['Sheet_Name'])

    def __del__(self):
        self._osignal.__del__()
        #self._indicator.__del__()
        self._wks = None
        self._importto = None

    def write(self, dictList):
        #if self._importto == enum.ImportTo.GSHEET:
            #self._wks.clear()
            index=[]
            tool=[]
            signal=[]
            date=[]
            price=[]
            onDate=[]
            for stockname, data in dictList.items():
                for i in range(len(data)):
                    index.append(stockname)
                    tool.append(data[i]['Tool'])
                    signal.append(data[i]['Signal'])
                    date.append(data[i]['Date'])
                    price.append(data[i]['Price'])
                    onDate.append(data[i]['OnDate'])

            d = {'Stock Name': pd.Series(index), 'Tool': pd.Series(tool), 'Signal': pd.Series(signal),'Date': pd.Series(date),\
                'Price': pd.Series(price), 'OnDate': pd.Series(onDate)}
            df = pd.DataFrame(d)
            self._wks.update([df.columns.values.tolist()] + df.values.tolist())
            self._wks.format('Z1:A1', {'textFormat': {'bold': True}})
            #for rows in records:
                #ticket = str(rows['symbol'])
                #market = str(rows['exchange'])
                #token = self.getTokenInfo(ticket)
                #list = self.constructlistjson(rows) 
                #list = self.__constructlist(ticket, market)
                #all_list.append(list)
        #return all_list
        
    def constructlistjson(self, row):
        trading_symbol = ""
        if row["exchange"] == "NSE":
            trading_symbol = row['symbol'] + ".NS"
        cjson = {"tradingsymbol" : trading_symbol}
        return cjson

    def ExportSignal(self):   
        print("**************Exporting**************")
        tradingList = self._osignal.GetAllSignals()
        #Write Trading List o/p
        if self._importto == enum.ImportTo.GSHEET:
            self._wks.clear()
            self.write(tradingList)
        print("**************Final*****************")
        return tradingList

    def CalulateTradingSignal(self, stockname, df, internal):
        if df['close'].isnull().all():
            return

        enddate = df['date'][len(df)-1]
        latestprice = df['close'][len(df)-1]
        df['sma_20'] = self._indicator.sma(df.close, 20)
        df['upper20_bb'], df['lower20_bb'] = self._indicator.bb(df['close'], df['sma_20'], 20)
        df['rsi_14'] = self._indicator.rsi(df['close'], 14)

        peekHL = peekHighLow.PeekHighLow(df)  

        if ienum.Indicators.MOVINGAVERAGE20.name in self._indicators:
            self._osignal.basedOnMovingAverage20(stockname, df, peekHL.getLastPeekHLLevel(), enddate, internal)
        if ienum.Indicators.RSI14_OverBoughtSold.name in self._indicators:
            self._osignal.basedOnRelativeStrenghtIndex14(stockname, df, enddate, internal)
        if ienum.Indicators.RSI14_DIVERGENCE.name in self._indicators:
            self._osignal.basedOnRSI14DivergenceLevel(stockname, df, enddate, internal)
        if ienum.Indicators.BBAND.name in self._indicators:
            self._osignal.basedOnBollingerBand(stockname, df, enddate, internal)
        if ienum.Indicators.TREND.name in self._indicators:
            self._osignal.basedOnPeekHighLowTrend(stockname, df, peekHL.findCurrentPriceTrend(latestprice), enddate, internal)
        if ienum.Indicators.SUPPORTRESISTENCE.name in self._indicators:
            self._osignal.basedOnPeekHighLowSR(stockname, df, peekHL.getLastPeekSRLevel(), enddate, internal)

        peekHL.__del__()

    def CalulateTradingSignalBasedOnPattern(self, stockname, df, internal):
        if df['close'].isnull().all():
            return

        enddate = df['date'][len(df)-1]
        latestprice = df['close'][len(df)-1]
        df['sma_20'] = self._indicator.sma(df.close, 20)
        df['sma_10'] = self._indicator.sma(df.close, 10)
        df['upper20_bb'], df['lower20_bb'] = self._indicator.bb(df['close'], df['sma_20'], 20)
        df['rsi_14'] = self._indicator.rsi(df['close'], 14)

        peekHL = peekHighLow.PeekHighLow(df)  

        self._osignal.basedOnWickReversalPattern(stockname, df, peekHL.findCurrentPriceTrend(latestprice), enddate, internal)
        self._osignal.basedOnExtremeReversalPattern(stockname, df, enddate, internal)
        self._osignal.basedOnOutsideReversalPattern(stockname, df, enddate, internal)
        self._osignal.basedOnDojiReversalPattern(stockname, df, enddate, internal)

        peekHL.__del__()

    def Progressing(self, processingdata, enddate, internalInfo):
        testFromDate = enddate - timedelta(days=self._backTestFromDay)
        testInterval = 1
        if internalInfo == enum.Interval.WEEKLY:
            testInterval = 7
        elif internalInfo == enum.Interval.MONTHLY:
            testInterval = 31

        if self._isTest:
            dayDiff =  enddate - testFromDate
        else: dayDiff = enddate - enddate
        toolbar_width = dayDiff.days
        # setup progressbar
        sys.stdout.write("[%s]" % (" " * toolbar_width))
        sys.stdout.flush()
        sys.stdout.write("\b" * (toolbar_width+1)) # return to start of line, after '['
        sys.stdout.write(internalInfo.name)
        for stockname, data in processingdata.items():
            if not self._isTest:
                df = pd.DataFrame.from_dict(data)              
                if df['close'].isnull().all():
                    continue
                #self.CalulateTradingSignal(stockname, df, internalInfo)
                self.CalulateTradingSignalBasedOnPattern(stockname, df, internalInfo)

                sys.stdout.write("-")
                sys.stdout.flush()

                continue
            
            enddatefrom = testFromDate
            prevLastEndDate = None
            while (enddatefrom <= enddate):
                testDataItems = [item for item in data if item['date'] <= enddatefrom] 
                enddatefrom += timedelta(days=testInterval)
                df = pd.DataFrame.from_dict(testDataItems) 
                if df['close'].isnull().all():
                    break     
                lastEndDate = df['date'][len(df)-1]   
                if prevLastEndDate != None and lastEndDate == prevLastEndDate:
                    continue      
                #self.CalulateTradingSignal(stockname, df, internalInfo)
                self.CalulateTradingSignalBasedOnPattern(stockname, df, internalInfo)
                prevLastEndDate = lastEndDate

                sys.stdout.write("-")
                sys.stdout.flush()

        sys.stdout.write("]\n") # this ends the progress bar

    def Calculate(self, startdate, enddate):
        #Get Stock List i/p
        #stockList = slist.StockList(enum.ExportFrom.GSHEET, self._isTest).get()

        if len(self._stockList) > 0:
            yahooAPI1 = yapi.YahooAPI(self._stockList)
            dailyData = yahooAPI1.history_data(start=startdate, end=enddate, interval="1d").GetResult()

            yahooAPI2 = yapi.YahooAPI(self._stockList)
            weeklyData = yahooAPI2.history_data(start=startdate, end=enddate, interval="1wk").GetResult()

            yahooAPI3 = yapi.YahooAPI(self._stockList)
            monthlyData = yahooAPI3.history_data(start=startdate, end=enddate, interval="1mo").GetResult()

            startdate15 = datetime.now() - timedelta(55)
            enddate15 = datetime.now() - timedelta(1)
            yahooAPI4 = yapi.YahooAPI(self._stockList)
            minutes15Data = yahooAPI4.history_data(start=startdate15, end=enddate15, interval="15m").GetResult()

            self.Progressing(dailyData, enddate, enum.Interval.DAILY)        
            self.Progressing(weeklyData, enddate, enum.Interval.WEEKLY)  
            self.Progressing(monthlyData, enddate, enum.Interval.MONTHLY) 
            self.Progressing(minutes15Data, enddate, enum.Interval.MINUTES_15)     
                           
        else: print('No stocks found in input file. Not able to process.')

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

def getbollingerbandtradinglist(source):
    trade_list = [] #empty list
    bollingerBandConfig = jsonHelper.getnodedata('BollingerBand')
    days = bollingerBandConfig['fromday']
    startdate = datetime.now() - timedelta(days)
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

def getbollingerbandtradinglist_local(source):
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