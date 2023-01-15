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
    df['sma_20'] = indicator.sma(df.close, 20)
    df['upper20_bb'], df['lower20_bb'] = indicator.bb(df['close'], df['sma_20'], 20)
    
    osignal.basedOnBollingerBand(stockname, df)

for stockname, data in oneMonthData.items():
    df = pd.DataFrame.from_dict(data)

    sr_call = peekHighLow.PeekHighLow(df)
    list = sr_call.getPeekHighLowWithSRPoints()
    firstSupportPrice =sr_call.firstSupportPrice()
    firstResitencePrice = sr_call.firstResitencePrice()
    highestHitResistenceLevel=sr_call.highestHitResistenceLevelPrice()
    highestHitSupportLevel=sr_call.highestHitSupportLevelPrice()
    highestPrice=sr_call.highestPrice()
    lowestPrice=sr_call.lowestPrice()
    lastRsesitencePrice=sr_call.lastRsesitencePrice()
    lastSupportPrice=sr_call.lastSupportPrice()
    print("firstSupportPrice = " + str(firstSupportPrice))
    print("firstResitencePrice = " + str(firstResitencePrice))
    print("highestHitResistenceLevel = " + str(highestHitResistenceLevel))
    print("highestHitSupportLevel = " + str(highestHitSupportLevel))
    print("highestPrice = " + str(highestPrice))
    print("lowestPrice = " + str(lowestPrice))
    print("lastRsesitencePrice = " + str(lastRsesitencePrice))
    print("lastSupportPrice = " + str(lastSupportPrice))

    osignal.basedOnPeekHighLowTrend(stockname, df)

print("**************Exporting**************")
tradingList = osignal.GetAllSignals()
#Write Trading List o/p
stockList = tlist.TradingList(cenum.ImportTo.GSHEET).write(tradingList)

osignal.__del__()
print("**************Final*****************")