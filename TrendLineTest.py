from datetime import datetime, timedelta
import Helper.StockList as slist
import Enum.CommonEnum as enum
import Utility.YahooAPI as yapi
import pandas as pd
import Finder.Indicators as tools
import Finder.PeekHighLow as peekHighLow
from collections import defaultdict
import pandas as pd
import Utility.GSheet as gsheet

startdate = datetime.now() - timedelta(365*8) - timedelta(20)
enddate = datetime.now() - timedelta(1)
stockList = slist.StockList(enum.ExportFrom.GSHEET, False).get()
if len(stockList) > 0:
    marketTrendList = defaultdict(list)
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
        checkContinueTrendCnt = 2
        marketTrend = peekHL.getMarketTrendLine(checkContinueTrendCnt)

        trend = {"Trend": marketTrend.name}
        marketTrendList[stockname].append(trend)

    index=[]
    trend=[]
    gs = gsheet.GSheet('OurTradingLogic')
    wks = gs.sheet('MarketTrend')
    for stockname, data in marketTrendList.items():
        for i in range(len(data)):
            index.append(stockname)
            trend.append(data[i]['Trend'])

    d = {'Stock Name': pd.Series(index), 'Trend': pd.Series(trend)}
    df = pd.DataFrame(d)
    wks.clear()
    wks.update([df.columns.values.tolist()] + df.values.tolist())
    wks.format('Z1:A1', {'textFormat': {'bold': True}})