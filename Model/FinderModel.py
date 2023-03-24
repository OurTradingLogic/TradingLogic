import Enum.CommonEnum as cenum

class MarketData:
    Date = None
    HighPrice = None
    LowPrice = None
    ClosePrice = None
    OpenPrice = None

class PeekHighLowModel: 
    def __init__(self, highPrice, lowPrice, closePrice, level, date, movingAverage20 = 0): 
        self.PeekLevel = level
        self.LowPrice = lowPrice
        self.HighPrice = highPrice
        self.ClosePrice = closePrice
        self.SMA_20 = movingAverage20
        self.Date = date

class PeekHighLowSRLevelModel:
    SRLevel = cenum.SRLevel.NONE
    SRPrice = 0
    SRName = str()
    SRBreakOutCount = 0

    def __init__(self, peekHighLow): 
        self.LowPrice = peekHighLow.LowPrice
        self.HighPrice = peekHighLow.HighPrice
        self.PeekLevel = peekHighLow.PeekLevel
        self.Date = peekHighLow.Date

class PeekHighLowRSIModel:
    def __init__(self, closePrice, level, date, rsi, overBoughtSold = cenum.OverBoughtSold.NONE): 
        self.PeekLevel = level
        self.ClosePrice = closePrice
        self.OverBoughtSold = overBoughtSold
        self.RSI = rsi
        self.Date = date

class RSIDivergenceModel:
    DivergenceLevel = cenum.DivergenceLevel.NONE
    DivergenceLevelName = str()
    def __init__(self, peekHighLowRSI): 
        self.ClosePrice = peekHighLowRSI.ClosePrice
        self.RSI = peekHighLowRSI.RSI
        self.PeekLevel = peekHighLowRSI.PeekLevel
        self.Date = peekHighLowRSI.Date
        self.OverBoughtSold = peekHighLowRSI.OverBoughtSold

class BollingerBandModel:
    Date = None
    HighPrice = None
    LowPrice = None
    ClosePrice = None
    OpenPrice = None
    UpperBand = None
    LowerBand = None
    SMA = None
    BB_BreakOutLevel = None
    BB_InLineLevel = None
    BB_OverHighLowLevel = None
    def __init__(self, date, high, low, close, open, uband, lband, sma, bb_breakout, bb_inline, bb_overhighlevel):
        self.Date = date
        self.HighPrice = high
        self.LowPrice = low
        self.ClosePrice = close
        self.OpenPrice = open
        self.UpperBand = uband
        self.LowerBand = lband
        self.SMA = sma
        self.BB_BreakOutLevel = bb_breakout
        self.BB_InLineLevel = bb_inline
        self.BB_OverHighLowLevel = bb_overhighlevel

    