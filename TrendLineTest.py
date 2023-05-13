from datetime import datetime, timedelta
import Helper.StockList as slist
import Enum.CommonEnum as enum
import Utility.YahooAPI as yapi
import pandas as pd
import Finder.Indicators as tools
import Finder.PeekHighLow as peekHighLow

startdate = datetime.now() - timedelta(365*8) - timedelta(20)
enddate = datetime.now() - timedelta(1)
stockList = slist.StockList(enum.ExportFrom.GSHEET, False).get()
if len(stockList) > 0:
    yahooAPI1 = yapi.YahooAPI(stockList)
    indicator = tools.Indicator()
    dailyData = yahooAPI1.history_data(start=startdate, end=enddate, interval="1d").GetResult()
    marketTrend = enum.Trend.NONE
    for stockname, data in dailyData.items():
        df = pd.DataFrame.from_dict(data)              
        if df['close'].isnull().all():
            continue
        indicator.loadBasic(df)
        peekHL = peekHighLow.PeekHighLow(df)
        latestprice = df['close'][len(df)-1]
        marketTrend = peekHL.getMarketTrendLine(2)