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
import time
import sys

#Get it from Config
exportToGSheetConfig = jsonHelper.getnodedata('ExportToGSheet')
days = exportToGSheetConfig['fromday']
#startdate = datetime.now() - timedelta(days)
startdate = datetime.now() - timedelta(365*5) - timedelta(20)
enddate = datetime.now() - 1

#Get Stock List i/p
stockList = slist.StockList(cenum.ExportFrom.GSHEET, isTest = False).get()

yahooAPI1 = yapi.YahooAPI(stockList)

enddateTesting = enddate - timedelta(days=366*2)
twoMinuteData = yahooAPI1.history_data(start=startdate, end=enddateTesting, interval="2m").GetResult()
endDateTesting = list(twoMinuteData.items())[0][1][-1]['date']
endDateTestingUpto = enddate
#endDateTestingUpto = enddateTesting + timedelta(days=366*1)

tradingList = tlist.TradingList(cenum.ImportTo.GSHEET, isTest= True)

dayDiff =  enddate - endDateTesting
toolbar_width = dayDiff.days
# setup progressbar
toolbar_width_avg = toolbar_width/100
sys.stdout.write("[%s]" % (" " * toolbar_width))
sys.stdout.flush()
sys.stdout.write("\b" * (toolbar_width+1)) # return to start of line, after '['

#try:
while (endDateTesting <= endDateTestingUpto):
    tradingList.CalulateTradingSignal(startdate,endDateTesting)
    endDateTesting += timedelta(days=1)

    sys.stdout.write("-")
    sys.stdout.flush()
#except Exception as e:
    #print("Exception " + str(e))

sys.stdout.write("]\n") # this ends the progress bar

tradingList.ExportSignal()
tradingList.__del__()



