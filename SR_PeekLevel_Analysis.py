from datetime import datetime, timedelta
import Helper.StockList as slist
import Enum.CommonEnum as enum
import Utility.YahooAPI as yapi
import pandas as pd
import Finder.Indicators as tools
import Finder.PeekHighLow as peekHighLow
#For Google Sheet Export
from collections import defaultdict
import pandas as pd
import Utility.GSheet as gsheet
import Utility.Constant as con

startdate = datetime.now() - timedelta(365*25) - timedelta(20)
enddate = datetime.now() - timedelta(1)
stockList = slist.StockList(enum.ExportFrom.GSHEET, False).get()
if len(stockList) > 0:
    marketTrendList = defaultdict(list)
    yahooAPI1 = yapi.YahooAPI(stockList)
    indicator = tools.Indicator()
    dailyData = yahooAPI1.history_data(start=startdate, end=enddate, interval="1mo").GetResult()
    #marketTrend = enum.Trend.NONE
    peekHL = None
    for stockname, data in dailyData.items():
        df = pd.DataFrame.from_dict(data)              
        if df['close'].isnull().all():
            continue
        indicator.loadBasic(df)
        peekHL = peekHighLow.PeekHighLow(df)
        getSR1 = peekHL.getPeekHighLowWithSRPoints()
        getSR2 = peekHL.getPeekHighLowSRPoints()
        latestprice = df['close'][len(df)-1]
        #marketTrend = peekHL.getMarketTrendLine()

        #volumn = df['volume']

        #For Google Sheet Export - add into list
        #rend = {"Date": peekHL.name, "PeekLevel": peekHL}
        #marketTrendList[stockname].append(trend)

        #testList = peekHL.getPeekHighLowList()
        testList = peekHL.getPeekHighLowWithSRPoints()
        for data1 in testList:
            trend = {"Date": data1.Date.strftime(con.DATE_FORMAT_YMD), "PeekLevel": data1.PeekLevel.name, "SRName": data1.SRName, "SRBreakOut": data1.SRBreakOutCount}
            marketTrendList[stockname].append(trend)

    #Google Sheet Export Code
    index=[]
    date=[]
    peekLevel=[]
    srName=[]
    srBreakCount=[]
    gs = gsheet.GSheet('OurTradingLogic')
    wks = gs.sheet('MarketTrend')
    for stockname, data in marketTrendList.items():
        for i in range(len(data)):
            index.append(stockname)
            date.append(data[i]['Date'])
            peekLevel.append(data[i]['PeekLevel'])
            srName.append(data[i]['SRName'])
            srBreakCount.append(data[i]['SRBreakOut'])

    d = {'Stock Name': pd.Series(index), 'Date': pd.Series(date), 'PeekLevel': pd.Series(peekLevel), 'SRName': pd.Series(srName),  'SRBreakOut': pd.Series(srBreakCount)}
    df = pd.DataFrame(d)
    wks.clear()
    wks.update([df.columns.values.tolist()] + df.values.tolist())
    wks.format('Z1:A1', {'textFormat': {'bold': True}})