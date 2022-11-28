import Utility.GSheet as gsheet
import Helper.TradingList as tlist
import Enum.CommonEnum as cenum
import Utility.Constant as cons
import pandas as pd
import Helper.StockList as slist
import Utility.YahooAPI as yapi
from datetime import datetime, timedelta
import Helper.JsonReader as jsonHelper
import Finder.Indicators as tools
import Finder.Signal as snal
from collections import defaultdict
import Finder.BollingerBand as bband

#Connect google sheet with help of goole service account setup
#gs = gsheet.GSheet(cons.GSHEET_FILE1)

#Get specific sheet name
#wks = gs.sheet(cons.GS_BBAND)

#wks.update('A1', 'Welcome to all')

#trade_list = tlist.getbollingerbandtradinglist(cenum.ExportFrom.EXCEL)

#df = pd.DataFrame(trade_list)

#wks.update([df.columns.values.tolist()] + df.values.tolist())

#Clear memory
#gs.__del__()

bollingerBandConfig = jsonHelper.getnodedata('BollingerBand')
fromdayBB = bollingerBandConfig['fromday']

exportToGSheetConfig = jsonHelper.getnodedata('ExportToGSheet')
days = exportToGSheetConfig['fromday']
startdate = datetime.now() - timedelta(days)
enddate = datetime.now()

#Get Stock List i/p
stockList = slist.StockList(cenum.ExportFrom.GSHEET).get()

yahooAPI = yapi.YahooAPI(stockList)
stocks = yahooAPI.history_data(start=startdate, end=enddate, interval="1wk").GetResult()

indicator = tools.Indicator()
osignal = snal.Signal()

for stockname, data in stocks.items():
    df = pd.DataFrame.from_dict(data)
    df['sma_20'] = indicator.sma(df.close, 20)
    df['upper20_bb'], df['lower20_bb'] = indicator.bb(df['close'], df['sma_20'], 20)
    
    osignal.basedOnBollingerBand(stockname, df, fromdayBB)

print("....................")
tradingList = osignal.GetAllSignals()
#Write Trading List o/p
stockList = tlist.TradingList(cenum.ImportTo.GSHEET).write(tradingList)

osignal.__del__()


print("**************Final*****************")