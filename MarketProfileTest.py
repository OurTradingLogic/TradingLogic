from datetime import datetime, timedelta
import Helper.StockList as slist
import Enum.CommonEnum as enum
import Utility.YahooAPI as yapi
import pandas as pd
import Finder.Indicators as tools
#import Finder.MarketProfile as marketProfile
#For Google Sheet Export
from collections import defaultdict
import pandas as pd
import Utility.GSheet as gsheet
import Utility.Constant as con
import os
import Finder.MarketProfile as mp

startdate = datetime.now() - timedelta(10)
enddate = datetime.now() - timedelta(1)
result = defaultdict(list)
stockList = slist.StockList(enum.ExportFrom.GSHEET, False).get()
if len(stockList) > 0:
    marketTrendList = defaultdict(list)
    yahooAPI1 = yapi.YahooAPI(stockList)
    indicator = tools.Indicator()
    dailyData = yahooAPI1.history_data(start=startdate, end=enddate, interval="15m").GetResult()

    mprofile = mp.MarketProfile(dailyData)

    test = mprofile.findMarketVolumnProfile()

    print(test)


    # i = 0
    # for stockname, data in dailyData.items():
    #     i = i + 1
    #     df = pd.DataFrame.from_dict(data)              
    #     if df['close'].isnull().all():
    #         continue

    #     result = mp.market_profile(stockname, df)
    #     #mp.volume_profile(stockname, df)

    #     if i == 1:
    #         break

#print(result)

#Google Sheet Export Code
# index=[]
# date=[]
# peekLevel=[]
# srName=[]
# srBreakCount=[]
# gs = gsheet.GSheet('OurTradingLogic')
# wks = gs.sheet('MarketTrend')
# for stockname, data in result.items():
#     for i in range(len(data)):
#         index.append(stockname)
#         date.append(data[i]['Date'])
#         peekLevel.append(data[i]['PeekLevel'])
#         srName.append(data[i]['SRName'])
#         srBreakCount.append(data[i]['SRBreakOut'])

# d = {'Stock Name': pd.Series(index), 'Date': pd.Series(date), 'PeekLevel': pd.Series(peekLevel), 'SRName': pd.Series(srName),  'SRBreakOut': pd.Series(srBreakCount)}
# df = pd.DataFrame(d)
# wks.clear()
# wks.update([df.columns.values.tolist()] + df.values.tolist())
# wks.format('Z1:A1', {'textFormat': {'bold': True}})