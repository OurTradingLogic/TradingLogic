import Enum.CommonEnum as cenum

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


    