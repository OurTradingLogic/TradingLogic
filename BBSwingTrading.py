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

startdate = datetime.now() - timedelta(365*8) - timedelta(20)
enddate = datetime.now() - timedelta(1)

tradingList = tlist.TradingList(cenum.ImportTo.GSHEET, isTest = True)
tradingList.Calculate(startdate,enddate)
tradingList.ExportSignal()
tradingList.__del__()