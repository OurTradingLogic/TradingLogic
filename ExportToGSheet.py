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
import Utility.AppsScriptAPI as appsapi

#Get it from Config
exportToGSheetConfig = jsonHelper.getnodedata('ExportToGSheet')
days = exportToGSheetConfig['fromday']
#startdate = datetime.now() - timedelta(days)
startdate = datetime.now() - timedelta(365*2) - timedelta(20)
enddate = datetime.now()

#startdate = datetime(2018, 5, 1, 0,0,0,0)
#enddate = datetime(2018, 12, 12,0,0,0,0)

tradingList = tlist.TradingList(cenum.ImportTo.GSHEET, isTest = False)
tradingList.Calculate(startdate,enddate)
tradingList.ExportSignal()
tradingList.__del__()

#appsapi.AppsScriptAPI().Execute()