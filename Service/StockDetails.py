import Helper.TradingList as tlist
import Enum.CommonEnum as cenum
from datetime import datetime, timedelta
import Helper.JsonReader as jsonHelper
import Helper.StockList as slist
import Enum.CommonEnum as enum
import Utility.YahooAPI as yapi
import pandas as pd
import Finder.Indicators as tools
import Finder.BollingerBand as bban
from collections import defaultdict
import Helper.StockList as slist
import Utility.YahooAPI as yapi
import numpy as np

def stockLiveDetails(data):
    stockDetails = defaultdict(list)
    stockList = slist.StockList(cenum.ExportFrom.JSONDATA, False, data).get()
    for stock in stockList:
        stockName = stock['tradingsymbol']
        price = yapi.get_live_price(stock['tradingsymbol'])
        if not np.isnan(price):
            details = {"Price": price}
            stockDetails[stockName + '.NS'] = details
    return stockDetails
