from pandas.core.base import NoNewAttributesMixin
from twisted import python
from Utility.SmartAPIConnect import SmartConnect
##import Utility
from datetime import datetime #to calculate the execution time
import time
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta
import pandas as pd
import Helper.StockList as com
import Utility.SmartAPI as sapi
import Helper.TradingList as tlist
import Enum.CommonEnum as cenum
import Utility.Constant as cons
import Utility.Excel as excel
import Utility.GSheet as gsheet
import yfinance as yf
import yahoo_fin as yfin
from yahoo_fin import stock_info as si

def getPivotPoint():
    trade_list = tlist.getpivotpointtradinglist("test")
    excel.WriteFromList(trade_list, cons.DATA_FOLDER+'PivotPointTradingList.xlsx')

def getBollingerBand():
    #trade_list = com.gettradinglist()
    #trade_list = com.getfromjson()
    trade_list = tlist.getbollingerbandtradinglist(cenum.ExportFrom.JSON)
    #print(trade_list)
    excel.WriteFromList(trade_list, cons.DATA_FOLDER+'TradingList.xlsx')


print(yfin.__version__)
print(yfin.__name__)
#getPivotPoint()

gs = gsheet.GSheet(cons.GSHEET_FILE1)
#Get specific sheet name
wks = gs.sheet(cons.GS_BBAND)

#wks.update('A1', 'Welcome to all')

trade_list = tlist.getbollingerbandtradinglist(cenum.ExportFrom.JSON)

df = pd.DataFrame(trade_list)

wks.update([df.columns.values.tolist()] + df.values.tolist())

#Get specific sheet name
gs.__del__()


print("**************Final*****************")

#verifying if the login was successful
#print(data)

#Order()

#obj = SmartConnect(api_key = "AccessKey")
#this obj will be used later on to make all the trade requests.

#Let's login
#data = obj.generateSession("Username","Password")

#for trades in trade_list:
    #sapi.place_order(obj, trades)

#sapi.Order(obj)

#obj.terminateSession("SessionId")



