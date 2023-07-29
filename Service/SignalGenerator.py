from flask import Flask, request, jsonify
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
from collections import defaultdict

def tradingSignal(data):
    result = defaultdict(list)
    startdate = datetime.now() - timedelta(365*8) - timedelta(20)
    enddate = datetime.now() - timedelta(1)

    tradingList = tlist.TradingList(cenum.ImportTo.JSONDATA, cenum.ExportFrom.JSONDATA, isTest = False, jsonData= data)

    tradingList.Calculate(startdate,enddate)
    result = tradingList.ExportSignal().copy()
    tradingList.__del__()

    return result
