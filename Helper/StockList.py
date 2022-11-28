from datetime import datetime, timedelta
import json
import pandas as pd
import Utility.YahooAPI as yapi
import Finder.BollingerBand as bband
import Enum.CommonEnum as enum
from requests import get
import Utility.Constant as cons
import Utility.GSheet as gsheet
import Helper.JsonReader as jsonHelper

class StockList:
    global token_ab
    url = "https://margincalculator.angelbroking.com/OpenAPI_File/files/OpenAPIScripMaster.json"
    d = get(url).json()
    token_ab = pd.DataFrame.from_dict(d)

    _exportFrom = enum.ExportFrom.NONE
    _wks = None
    def __init__(self, exportFrom):
        self._exportFrom = exportFrom
        if exportFrom == enum.ExportFrom.GSHEET:
            gSheetStockListConfig = jsonHelper.getnodedata('GSheet_StockList')
            gs = gsheet.GSheet(gSheetStockListConfig['File_Name'])
            self._wks = gs.sheet(gSheetStockListConfig['Sheet_Name'])

    def get(self):
        all_list = [] #empty list
        if self._exportFrom == enum.ExportFrom.GSHEET:
            records = self._wks.get_all_records()
            
            for rows in records:
                ticket = str(rows['symbol'])
                market = str(rows['exchange'])
                #token = self.getTokenInfo(ticket)
                #list = self.constructlistjson(rows) 
                list = self.__constructlist(ticket, market)
                all_list.append(list)
        return all_list

    def __constructlist(self, symbol, exchange):
        dict = {"tradingsymbol" : str(symbol),
                "exchange": str(exchange)}
        return dict

    def getTokenInfo(self, symbol):
        if symbol == "ADANIPOWER":
            symbol = symbol + "-BE"
        else:
            symbol = symbol + "-EQ"

        df_script = token_ab.loc[token_df['symbol'] == symbol]
        if not df_script.empty:
            return df_script.iat[0,0]
        else:
            return "0"

pd.options.mode.chained_assignment = None

global token_df
url = "https://margincalculator.angelbroking.com/OpenAPI_File/files/OpenAPIScripMaster.json"
d = get(url).json()
token_df = pd.DataFrame.from_dict(d)

def getlistfrom(source):
    all_list = [] #empty list
    if source == enum.ExportFrom.EXCEL:
        all_list = getfromexcel()
    elif source == enum.ExportFrom.JSON:
        all_list = getfromjson()
    elif source == enum.ExportFrom.GSHEET:
        all_list = getFromGSheet()
    return all_list

def getfromjson():
    all_list = [] #empty list
    for index, rows in token_df.iterrows():
        name = rows["name"]
        symbol = rows["symbol"]
        if name + "-EQ" == symbol:
            list = constructlistjson(name, rows["token"], rows["exch_seg"]) 
            all_list.append(list)
    return all_list

def getfromexcel():
    all_list = [] #empty list
    df = pd.read_excel(cons.DATA_FOLDER+"Untitled.xlsx")
    for index, rows in df.iterrows():    
        ticket = str(rows['symbol'])
        list = constructlistjson(ticket, str(getTokenInfo(ticket)), str(rows['exchange'])) 
        all_list.append(list)
    return all_list

def getFromGSheet():
    all_list = [] #empty list

def getfrompivotpointexcel():
    all_list = [] #empty list
    df = pd.read_excel(cons.DATA_FOLDER + "PivotPointTradingList.xlsx")
    for index, rows in df.iterrows():    
        ticket = str(rows['tradingsymbol'])
        list = constructlistjson(ticket, str(getTokenInfo(ticket)), str(rows['exchange'])) 
        all_list.append(list)
    return all_list

def getfromjsondata(node):
    all_list = [] #empty list
    f = open(cons.DATA_FOLDER+cons.DATA_JSON, 'r')
    load = json.load(f)

    for data in load[node]:    
      ticket = str(data['symbol'])
      list = constructlistjson(ticket, str(getTokenInfo(ticket)), str(data['exchange'])) 
      all_list.append(list)
    return all_list

def getTokenInfo(symbol):
    if symbol == "ADANIPOWER":
        symbol = symbol + "-BE"
    else:
        symbol = symbol + "-EQ"

    df_script = token_df.loc[token_df['symbol'] == symbol]
    if not df_script.empty:
        return df_script.iat[0,0]
    else:
        return "0"

def constructorderjson(row, latestprice):
    cjson = {"variety": "NORMAL", 
            "tradingsymbol" : str(row["tradingsymbol"]),
            "symboltoken" : str(row["symboltoken"]),
            "transactiontype": "BUY", 
            "exchange": str(row["exchange"]),
            "ordertype": "MARKET", 
            "producttype": "AMO Delivery",
            "duration": "DAY", 
            "price": str(latestprice), 
            "quantity": "1",
            "triggerprice": "0"}
    return cjson

def constructlistjson(symbol, token, exchange):
    cjson = {"tradingsymbol" : str(symbol),
            "symboltoken" : str(token),
            "exchange": str(exchange)}
    return cjson

def constructpivotpointjson(row, pp, r1, s1, r2, s2, r3, s3, r4, s4):
    cjson = {"tradingsymbol" : str(row["tradingsymbol"]),
            "symboltoken" : str(row["symboltoken"]),
            "exchange": str(row["exchange"]),
            "CPR": str(pp),
            "R1": str(r1),
            "S1": str(s1),
            "R2": str(r2),
            "S2": str(s2),
            "R3": str(r3),
            "S3": str(s3),
            "R4": str(r4),
            "S4": str(s4)}
    return cjson