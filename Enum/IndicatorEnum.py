from enum import Enum
from lib2to3.pgen2.token import EQUAL

class Indicators(Enum):
    BBAND = 1
    NONE = 0

class BB_BreakOut(Enum):
    UPPER_BB = 1
    LOWER_BB = 2
    NONE = 0

class BB_InLine(Enum):
    UPPER_BB_LINE = 1,
    LOWER_BB_LINE = 2,
    SMA_LINE = 3,
    NONE = 0