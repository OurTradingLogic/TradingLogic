from pandas.core.base import NoNewAttributesMixin
from twisted import python
from SmartAPIConnect import SmartConnect
from datetime import datetime #to calculate the execution time
import time
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta
import pandas as pd
import StockList as com
import SmartAPI as sapi
import TradingList as tlist
import CommonEnum as cenum
import xlsxwriter 


def getPivotPoint():
    trade_list = tlist.getpivotpointtradinglist("test")
    with xlsxwriter.Workbook('PivotPointTradingList.xlsx') as workbook:
        worksheet = workbook.add_worksheet()

        for row_num, data in enumerate(trade_list):
            colnum = 0
            if row_num == 0:
                worksheet.write_row(row_num, 0, data)

            for item in data:
                worksheet.write(row_num+1, colnum, data[item])
                colnum = colnum + 1

def getBollingerBand():
    #trade_list = com.gettradinglist()
    #trade_list = com.getfromjson()
    trade_list = tlist.gettradinglist(cenum.ExportFrom.JSON)
    #print(trade_list)

    with xlsxwriter.Workbook('TradingList.xlsx') as workbook:
        worksheet = workbook.add_worksheet()

        for row_num, data in enumerate(trade_list):
            colnum = 0
            if row_num == 0:
                worksheet.write_row(row_num, 0, data)

            for item in data:
                worksheet.write(row_num+1, colnum, data[item])
                colnum = colnum + 1

getPivotPoint()
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



