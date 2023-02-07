import Enum.CommonEnum as enum
import Model.FinderModel as fmodel
from operator import attrgetter

class RelativeStrengthIndex:
    def __init__(self, data, overBoughtLevel = 70, overSoldLevel = 30, trendCountCheck = 2):
        self.overBoughtLevel = overBoughtLevel
        self.overSoldLevel = overSoldLevel
        self.PEEK_HIGH_LOW_TREND_COUNT = trendCountCheck
        self.__hl_list = []
        self.__load(data)
        self.__divergenceLevel_loaded = False
        self.__DivergenceLevel_list = []

    def __del__(self):
        self.__divergenceLevel_loaded = False
        self.__hl_list.clear()
        self.__DivergenceLevel_list.clear()

    def __load(self,data):
        trend = enum.Trend.NONE
        preTrend = enum.Trend.NONE
        trendContinueCnt = 0
        close_price = 0
        rsi_14 = 0
        date = None
        hl_list = []
        hl_close_price = 0
        hl_date = None
        hl_rsi = 0
        prev_close_price = None
        prev_date = None
        prev_rsi = 0

        for i in range(len(data)):
            close_price = data['close'][i]
            date = data['date'][i]
            rsi_14 = data['rsi_14'][i]

            """ First 20, we can ignore that for calculating correct rsi_14 value"""
            if i < 21:
                continue

            if prev_close_price != None:  
                if prev_close_price < close_price:                 
                    trend = enum.Trend.UP
                elif prev_close_price > close_price: 
                    trend = enum.Trend.DOWN
                else:
                    trend = enum.Trend.STRAIGHT

                if self.PEEK_HIGH_LOW_TREND_COUNT == 0:
                    hl_close_price = close_price
                    hl_date = date
                    hl_rsi = rsi_14
                else:
                    if (preTrend == trend or trend == enum.Trend.STRAIGHT) and trend != enum.Trend.NONE:
                        trendContinueCnt = trendContinueCnt + 1
                    else:
                        trendContinueCnt = 0
                        hl_close_price = prev_close_price
                        hl_date = prev_date
                        hl_rsi =  prev_rsi

                if trend == enum.Trend.UP or trend == enum.Trend.DOWN:
                    preTrend = trend

                if trendContinueCnt == self.PEEK_HIGH_LOW_TREND_COUNT:
                    overBoughtSold = enum.OverBoughtSold.NONE
                    
                    if rsi_14 >= self.overBoughtLevel:
                        overBoughtSold = enum.OverBoughtSold.OVERBOUGHT
                    elif rsi_14 <= self.overSoldLevel:
                        overBoughtSold = enum.OverBoughtSold.OVERSOLD

                    if trend == enum.Trend.UP:
                        hl_list.append(fmodel.PeekHighLowRSIModel(hl_close_price, enum.PeekLevel.LOW, hl_date, hl_rsi, overBoughtSold))
                        #print("Added close Price UP =" + str(hl_close_price) + " Date = " + str(hl_date))
                    elif trend == enum.Trend.DOWN:
                        hl_list.append(fmodel.PeekHighLowRSIModel(hl_close_price, enum.PeekLevel.HIGH, hl_date, hl_rsi, overBoughtSold))
                        #print("Added close Price DOWN =" + str(hl_close_price) + " Date = " + str(hl_date))

            prev_close_price = close_price
            prev_date = date
            prev_rsi = rsi_14

        self.__hl_list = hl_list

    def Reload(self, data):
        self.__hl_list.clear()
        self.__load(data) 

    def getOverBoughtSoldPeekLevels(self):
        overBoughtSoldList =  [item for item in self.__hl_list if item.OverBoughtSold != enum.OverBoughtSold.NONE] 
        return overBoughtSoldList

    def getLastOverBoughtSoldPeekLevel(self):
        getOverBoughtSoldPeekLevels = self.getOverBoughtSoldPeekLevels()
        return getOverBoughtSoldPeekLevels[-1]

    def __calculateDivergencePoints(self, waitingCount = 2): 
        overBoughtSoldDivergenceList = [] 
        bearishDivergenceCount = 0
        bullishDivergenceCount = 0

        firstOverBoughtSoldPoint = None
        firstOverBoughtSoldPointFound = 0
        for hl in self.__hl_list: 

            if firstOverBoughtSoldPoint != None:
                firstOverBoughtSoldPointFound+=1
                if firstOverBoughtSoldPoint.PeekLevel == hl.PeekLevel:
                    if firstOverBoughtSoldPoint.OverBoughtSold == enum.OverBoughtSold.OVERSOLD and \
                        hl.OverBoughtSold == firstOverBoughtSoldPoint.OverBoughtSold and hl.PeekLevel == firstOverBoughtSoldPoint.PeekLevel and \
                        firstOverBoughtSoldPoint.RSI < hl.RSI:
                        bullishDivergenceCount+=1
                        hlCurrent = fmodel.RSIDivergenceModel(hl) 
                        hlCurrent.DivergenceLevel = firstOverBoughtSoldPoint.DivergenceLevel = enum.DivergenceLevel.BULLISH
                        hlCurrent.DivergenceLevelName = firstOverBoughtSoldPoint.DivergenceLevelName = enum.DivergenceLevel.BULLISH.name + str(bullishDivergenceCount)                      
                        overBoughtSoldDivergenceList.append(firstOverBoughtSoldPoint)
                        overBoughtSoldDivergenceList.append(hlCurrent)
                        firstOverBoughtSoldPointFound = 0
                        firstOverBoughtSoldPoint = None  
                    elif firstOverBoughtSoldPoint.OverBoughtSold == enum.OverBoughtSold.OVERBOUGHT and \
                        hl.OverBoughtSold == firstOverBoughtSoldPoint.OverBoughtSold and hl.PeekLevel == firstOverBoughtSoldPoint.PeekLevel and \
                        firstOverBoughtSoldPoint.RSI > hl.RSI:
                        bearishDivergenceCount+=1
                        hlCurrent = fmodel.RSIDivergenceModel(hl) 
                        hlCurrent.DivergenceLevel = firstOverBoughtSoldPoint.DivergenceLevel = enum.DivergenceLevel.BEARISH
                        hlCurrent.DivergenceLevelName = firstOverBoughtSoldPoint.DivergenceLevelName = enum.DivergenceLevel.BEARISH.name + str(bearishDivergenceCount)
                        overBoughtSoldDivergenceList.append(firstOverBoughtSoldPoint)
                        overBoughtSoldDivergenceList.append(hlCurrent)
                        firstOverBoughtSoldPointFound = 0
                        firstOverBoughtSoldPoint = None  
            
            if hl.OverBoughtSold != enum.OverBoughtSold.NONE:
                if firstOverBoughtSoldPoint == None:
                    firstOverBoughtSoldPoint = fmodel.RSIDivergenceModel(hl)                   
            else: 
                if firstOverBoughtSoldPointFound == 0 or firstOverBoughtSoldPointFound > waitingCount:
                    firstOverBoughtSoldPoint = None                  

        self.__DivergenceLevel_list = overBoughtSoldDivergenceList

    def __loadDivergencePoint_list(self):
        if not self.__divergenceLevel_loaded:
            self.__calculateDivergencePoints()
            self.__divergenceLevel_loaded = True

    def getRSIDivergencePoints(self):    
        self.__loadDivergencePoint_list()  
        divergencePoint = self.__DivergenceLevel_list.copy() 
        divergencePoint.sort(key=attrgetter('DivergenceLevelName'))
        return divergencePoint

    def getBEARISHDivergencePoints(self):    
        divergencePoint = self.getRSIDivergencePoints()
        return [item for item in divergencePoint if item.DivergenceLevel == enum.DivergenceLevel.BEARISH] 

    def getBULLISHDivergencePoints(self):     
        divergencePoint = self.getRSIDivergencePoints()
        return [item for item in divergencePoint if item.DivergenceLevel == enum.DivergenceLevel.BULLISH]

    def getLastBEARISHDivergencePoints(self):     
        bearishDivergencePoint = self.getBEARISHDivergencePoints()
        return bearishDivergencePoint[-1]

    def getLastBULLISHDivergencePoints(self):    
        bullishDivergencePoint = self.getBULLISHDivergencePoints()
        return bullishDivergencePoint[-1]
    
    def getPeekHighLowList(self):
        return self.__hl_list