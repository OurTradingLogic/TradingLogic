import numpy as np
from enum import Enum
import math
from termcolor import colored as cl 
from numpy.lib.function_base import average
import Enum.IndicatorEnum as ienum 
import Enum.CommonEnum as cenum

class Indicator:
    def sma(self, data, window):
        sma = data.rolling(window = window).mean()
        return sma

    def bb(self, data, sma, window):
        std = data.rolling(window = window).std()
        upper_bb = sma + std * 2
        lower_bb = sma - std * 2
        return upper_bb, lower_bb