import Helper.TradingList as tlist
import Enum.CommonEnum as cenum
from datetime import datetime, timedelta
from collections import defaultdict

result = defaultdict(list)
startdate = datetime.now() - timedelta(365*8) - timedelta(20)
enddate = datetime.now() - timedelta(1)

tradingList = tlist.TradingList(cenum.ImportTo.GSHEET, cenum.ExportFrom.GSHEET, isTest = False, jsonData= '')

tradingList.Calculate(startdate,enddate)
result = tradingList.ExportSignal().copy()
tradingList.__del__()