import Helper.TradingList as tlist
import Enum.CommonEnum as cenum
from datetime import datetime, timedelta
import Helper.JsonReader as jsonHelper
import Helper.StockList as slist
import Enum.CommonEnum as enum
import Utility.YahooAPI as yapi
import pandas as pd
import Finder.Indicators as tools
import Finder.BollingerBand as bband

startdate = datetime.now() - timedelta(365*2) - timedelta(20)
enddate = datetime.now() - timedelta(1)

stockList = slist.StockList(enum.ExportFrom.GSHEET, False).get()
if len(stockList) > 0:
    yahooAPI1 = yapi.YahooAPI(stockList)
    dailyData = yahooAPI1.history_data(start=startdate, end=enddate, interval="1d").GetResult()
    _indicator =  tools.Indicator()
    for stockname, data in dailyData.items():
        df = pd.DataFrame.from_dict(data)              
        if df['close'].isnull().all():
            continue
        onDate = df['date'][len(df)-1]
        df['sma_20'] = _indicator.sma(df.close, 20)
        df['upper20_bb'], df['lower20_bb'] = _indicator.bb(df['close'], df['sma_20'], 20)

        bbandObject = bband.BollingerBand(df) 
        lastBBOverHighLowLevel = bbandObject.getLastOverHighLowLevel(onDate)
        findBollingerBandTrend = bbandObject.findBollingerBandTrend(onDate)
        getOverHighLowLevels = bbandObject.getOverHighLowLevels()
        getBreakOutLevels = bbandObject.getBreakOutLevels()
        getBBInLineLevels = bbandObject.getBBInLineLevels()




#tradingList = tlist.TradingList(cenum.ImportTo.GSHEET, isTest = False)
#tradingList.Calculate(startdate,enddate)
#tradingList.ExportSignal()
#tradingList.__del__()