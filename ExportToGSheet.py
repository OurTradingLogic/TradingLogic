import Helper.TradingList as tlist
import Enum.CommonEnum as cenum
import pandas as pd
import Helper.StockList as slist
import Utility.YahooAPI as yapi
from datetime import datetime, timedelta
import Helper.JsonReader as jsonHelper
import Finder.Indicators as tools
import Finder.Signal as snal
import Finder.PeekHighLow as peekHighLow
import Finder.RelativeStrengthIndex as rsi

#Get it from Config
exportToGSheetConfig = jsonHelper.getnodedata('ExportToGSheet')
days = exportToGSheetConfig['fromday']
#startdate = datetime.now() - timedelta(days)
startdate = datetime.now() - timedelta(365*36) - timedelta(20)
enddate = datetime.now()

#Get Stock List i/p
stockList = slist.StockList(cenum.ExportFrom.GSHEET).get()

yahooAPI1 = yapi.YahooAPI(stockList)
oneWeekData = yahooAPI1.history_data(start=startdate, end=enddate, interval="1wk").GetResult()

yahooAPI2 = yapi.YahooAPI(stockList)
oneMonthData = yahooAPI2.history_data(start=startdate, end=enddate, interval="1mo").GetResult()

indicator = tools.Indicator()
osignal = snal.Signal()

for stockname, data in oneWeekData.items():
    df = pd.DataFrame.from_dict(data)
    if df['close'].isnull().all():
        continue
    df['sma_20'] = indicator.sma(df.close, 20)
    df['upper20_bb'], df['lower20_bb'] = indicator.bb(df['close'], df['sma_20'], 20)
    df['rsi_14'] = indicator.rsi(df['close'], 14)
    peekHL = peekHighLow.PeekHighLow(df)  

    osignal.basedOnBollingerBand(stockname, df)
    osignal.basedOnMovingAverage20(stockname, df, peekHL.getLastPeekHLLevel())

    peekHL.__del__()

for stockname, data in oneMonthData.items():
    df = pd.DataFrame.from_dict(data)
    if df['close'].isnull().all():
        continue

    latestprice = df['close'][len(df)-1]
    df['sma_20'] = indicator.sma(df.close, 20)
    df['upper20_bb'], df['lower20_bb'] = indicator.bb(df['close'], df['sma_20'], 20)
    df['rsi_14'] = indicator.rsi(df['close'], 14)
    peekHL = peekHighLow.PeekHighLow(df)

    #rsicall = rsi.RelativeStrengthIndex(df, trendCountCheck = 0)
    #tradelist = rsicall.getBEARISHDivergencePoints()
    #tradelist2 = rsicall.getBULLISHDivergencePoints()
    #tradelist3 = rsicall.getLastBEARISHDivergencePoints()
    #tradelist4 = rsicall.getLastBULLISHDivergencePoints()

    osignal.basedOnPeekHighLowTrend(stockname, df, peekHL.findCurrentTrend(latestprice))
    osignal.basedOnPeekHighLowSR(stockname, df, peekHL.getLastPeekSRLevel())
    peekHL.__del__()

print("**************Exporting**************")
tradingList = osignal.GetAllSignals()
#Write Trading List o/p
stockList = tlist.TradingList(cenum.ImportTo.GSHEET).write(tradingList)

osignal.__del__()
print("**************Final*****************")