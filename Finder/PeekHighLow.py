import Enum.CommonEnum as enum
import Finder.CandleStick as candle
import Utility.Common as cmethod
import Model.FinderModel as fmodel
import numpy as np
from operator import attrgetter
import itertools
from datetime import datetime, timedelta

class PeekHighLow:
    PEEK_HIGH_LOW_TREND_COUNT = 2

    def __init__(self,data):
        self.__hl_list = []
        self.__load(data)
        self.__srLevel_loaded = False
        self.__hl_SRLevel_list = []
        self.__SRLevel_list = []

    def __del__(self):
        self.__srLevel_loaded = False
        self.__hl_list.clear()
        self.__hl_SRLevel_list.clear()
        self.__SRLevel_list.clear()
    
    def __load(self,data):
        trend = enum.Trend.NONE
        preTrend = enum.Trend.NONE
        trendContinueCnt = 0
        open_price = 0
        close_price = 0
        high_price = 0
        low_price = 0
        prev_open_price = 0
        prev_close_price = 0
        prev_high_price = 0
        prev_low_price = 0
        hl_open_price = 0
        hl_close_price = 0
        hl_high_price = 0
        hl_low_price = 0
        hl_date = None
        prev_date = None
        hl_list = []

        for i in range(len(data)):
            open_price = data['open'][i]
            close_price = data['close'][i]
            high_price = data['high'][i]
            low_price = data['low'][i]
            date = data['date'][i]

            if i > 0:
                trend = candle.getTrend(prev_open_price, prev_close_price, close_price)
                if (preTrend == trend or trend == enum.Trend.STRAIGHT) and trend != enum.Trend.NONE:
                    trendContinueCnt = trendContinueCnt + 1
                else:
                    trendContinueCnt = 0
                    hl_open_price = prev_open_price
                    hl_close_price = prev_close_price
                    hl_high_price = prev_high_price
                    hl_low_price = prev_low_price
                    hl_date = prev_date

                if trend == enum.Trend.UP or trend == enum.Trend.DOWN:
                    preTrend = trend

            if trendContinueCnt == self.PEEK_HIGH_LOW_TREND_COUNT:
                if trend == enum.Trend.UP:
                    hl_list.append(fmodel.PeekHighLowModel(hl_high_price, hl_low_price, hl_close_price, enum.PeekLevel.LOW, hl_date))
                    #print("Added Lowest Price " + str(hl_low_price) + " Date = " + str(hl_date))
                elif trend == enum.Trend.DOWN:
                    hl_list.append(fmodel.PeekHighLowModel(hl_high_price, hl_low_price, hl_close_price, enum.PeekLevel.HIGH, hl_date))
                    #print("Added Highest Price " + str(hl_high_price) + " Date = " + str(hl_date))
            
            if open_price == np.nan:
                prev_open_price = prev_close_price
            else:
                prev_open_price = open_price
            prev_close_price = close_price
            prev_high_price = high_price
            prev_low_price = low_price
            prev_date = date

        self.__hl_list = hl_list

    def Reload(self, data):
        self.__hl_list.clear()
        self.__load(data)    

    def __calculateSRPoints(self):
        srList = [] 
        sCount = 0
        rCount = 0
        for hl in self.__hl_list: 
            srCurrent = fmodel.PeekHighLowSRLevelModel(hl) 

            for srExisting in srList:  #[:-1]
                peekLevelExisting = srExisting.PeekLevel
                peekLevelCurrent = srCurrent.PeekLevel
                highPriceCurrent = srCurrent.HighPrice
                lowPriceCurrent = srCurrent.LowPrice
                peekPriceExisting = 0
                inRange = False
                if peekLevelExisting == enum.PeekLevel.LOW:
                    peekPriceExisting = srExisting.LowPrice
                elif peekLevelExisting == enum.PeekLevel.HIGH:
                    peekPriceExisting = srExisting.HighPrice

                if cmethod.InRange(highPriceCurrent, lowPriceCurrent, peekPriceExisting): 
                    inRange = True

                if inRange:
                    if peekLevelExisting == peekLevelCurrent:
                        if peekLevelCurrent == enum.PeekLevel.LOW:
                            srExisting.SRLevel = srCurrent.SRLevel = enum.SRLevel.SUPPORT                       
                            
                            if not srExisting.SRName:
                                sCount+=1
                                srExisting.SRName = srCurrent.SRName = srCurrent.SRLevel.name + str(sCount)
                                srExisting.SRPrice = srExisting.LowPrice

                            srCurrent.SRName = srExisting.SRName
                            srCurrent.SRPrice = srExisting.SRPrice
                            #print(str(srCurrent.SRName) + " Support at " + str(lowPriceCurrent) + " Date = " + str(srCurrent.Date))
                            #print('-------Existing: '+str(srExisting.Date))
                            break
                        elif peekLevelCurrent == enum.PeekLevel.HIGH:
                            srExisting.SRLevel = srCurrent.SRLevel = enum.SRLevel.RESISTENCE

                            if not srExisting.SRName:
                                rCount+=1
                                srExisting.SRName = srCurrent.SRName = srCurrent.SRLevel.name + str(rCount)
                                srExisting.SRPrice = srExisting.HighPrice                         
                            
                            srCurrent.SRName = srExisting.SRName
                            srCurrent.SRPrice = srExisting.SRPrice
                            #print(str(srCurrent.SRName) + " Resistence at " + str(highPriceCurrent) + " Date = " + str(srCurrent.Date))
                            #print('-------Existing: '+str(srExisting.Date))
                            break
                else:
                    if peekLevelExisting == peekLevelCurrent:
                        if (srExisting.SRLevel == enum.SRLevel.SUPPORT and peekPriceExisting > lowPriceCurrent) or \
                        (srExisting.SRLevel == enum.SRLevel.RESISTENCE and peekPriceExisting < highPriceCurrent):
                            srExisting.SRBreakOutCount+=1
                            #print("Break at " + str(srExisting.SRName) + " Date = " + str(srCurrent.Date))
                
            srList.append(srCurrent)

        self.__hl_SRLevel_list = srList

    def __loadSRLevel_list(self):
        if not self.__srLevel_loaded:
            self.__calculateSRPoints()
            result = [item for item in self.__hl_SRLevel_list if item.SRLevel != enum.SRLevel.NONE] 
            self.__SRLevel_list = result
            self.__srLevel_loaded = True

    def getPeekHighLowWithSRPoints(self):    
        self.__loadSRLevel_list()  
        return self.__hl_SRLevel_list

    def getPeekHighLowSRPoints(self):    
        self.__loadSRLevel_list()  
        return self.__SRLevel_list

    def getPeekHighLowList(self):
        return self.__hl_list

    def highestPrice(self):
        result = max(self.__hl_list, key=attrgetter('HighPrice'))
        return result.HighPrice

    def lowestPrice(self):
        result = min(self.__hl_list, key=attrgetter('LowPrice'))
        return result.LowPrice

    def lastSupportPrice(self):
        self.__loadSRLevel_list()
        supportList = [item for item in self.__SRLevel_list if item.SRLevel == enum.SRLevel.SUPPORT] 
        supportLevel = supportList[-1]
        return supportLevel.LowPrice

    def lastRsesitencePrice(self):
        self.__loadSRLevel_list()
        resistenceList = [item for item in self.__SRLevel_list if item.SRLevel == enum.SRLevel.RESISTENCE] 
        resistenceLevel = resistenceList[-1]
        return resistenceLevel.HighPrice

    def firstSupportPrice(self):
        self.__loadSRLevel_list()
        supportList = [item for item in self.__SRLevel_list if item.SRLevel == enum.SRLevel.SUPPORT] 
        supportLevel = supportList[0]
        return supportLevel.LowPrice

    def firstResitencePrice(self):
        self.__loadSRLevel_list()
        resistenceList = [item for item in self.__SRLevel_list if item.SRLevel == enum.SRLevel.RESISTENCE] 
        resistenceLevel = resistenceList[0]
        return resistenceLevel.HighPrice

    def highestHitSupportLevelPrice(self):
        self.__loadSRLevel_list()
        supportList = [item for item in self.__SRLevel_list if item.SRLevel == enum.SRLevel.SUPPORT] 
        #supportList.sort(key=attrgetter('SRName'))

        curr_count = 0
        prev_count = 0
        srName = str()
        srgroupList = {}
        #for k, g in itertools.groupby(sorted(supportList, key=attrgetter('SRName')), key=attrgetter('SRName')):
        for k, g in itertools.groupby(supportList, key=attrgetter('SRName')):
            srgroupList[k] = list(g)

        for k, srList in srgroupList.items():         
            curr_count = len(srList)
            if curr_count > prev_count:
                srName = k
            prev_count = curr_count

        highestHitSupportLevel = None
        if srName:
            highestHitSupportLevel = [item for item in supportList if item.SRName == srName][0]

        return highestHitSupportLevel.LowPrice

    def highestHitResistenceLevelPrice(self):
        self.__loadSRLevel_list()
        resistenceList = [item for item in self.__SRLevel_list if item.SRLevel == enum.SRLevel.RESISTENCE] 
        #resistenceList.sort(key=attrgetter('SRName'))

        curr_count = 0
        prev_count = 0
        srName = str()
        srgroupList = {}
        #for k, g in itertools.groupby(sorted(resistenceList, key=attrgetter('SRName')), key=attrgetter('SRName')):
        for k, g in itertools.groupby(resistenceList, key=attrgetter('SRName')):
            srgroupList[k] = list(g)

        for k, srList in srgroupList.items():         
            curr_count = len(srList)
            if curr_count > prev_count:
                srName = k
            prev_count = curr_count

        highestHitResistenceLevel = None
        if srName:
            highestHitResistenceLevel = [item for item in resistenceList if item.SRName == srName][0]

        return highestHitResistenceLevel.HighPrice

    def findCurrentTrend(self, price):
        result = enum.Trend.NONE
        hl = self.__hl_list[-1]
        if price > hl.ClosePrice:
            if hl.PeekLevel == enum.PeekLevel.LOW:
                result = enum.Trend.UP
            else: result = enum.Trend.REVERSE
        elif price < hl.ClosePrice:
            if hl.PeekLevel == enum.PeekLevel.HIGH:   
                result = enum.Trend.DOWN 
            else: result = enum.Trend.REVERSE 
        else: result = enum.Trend.STRAIGHT 
        
        return result 