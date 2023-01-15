from enum import Enum
from lib2to3.pgen2.token import EQUAL

class ExportFrom(Enum):
  EXCEL = 1
  JSON = 2
  WEB = 3
  GSHEET = 4
  NONE = 0 

class ImportTo(Enum):
  EXCEL = 1
  JSON = 2
  WEB = 3
  GSHEET = 4
  NONE = 0 

class PeekLevel(Enum):
  HIGH = 1
  LOW = 2
  NONE = 0

class SRLevel(Enum):
  SUPPORT = 1
  RESISTENCE = 2
  NONE = 0

class InLine(Enum):
  SUPPORT = 1
  RESISTENCE = 2
  NONE = 0

class InLineSR(Enum):
  S1 = 1
  R1 = 2
  S2 = 3
  R2 = 4
  S3 = 5
  R3 = 6
  S4 = 7
  R4 = 8
  NONE = 0

class Trend(Enum):
  UP = 1
  DOWN = 2
  STRAIGHT = 3
  REVERSE = 4
  NONE = 0

class Position(Enum):
  CPR = 1
  S12 = 2
  S23 = 3
  S34 = 4
  R12 = 5
  R23 = 6
  R34 = 7
  NONE = 0

  class Travel(Enum):
    CPR = 1
    S12 = 2
    S23 = 3
    S34 = 4
    R12 = 5
    R23 = 6
    R34 = 7
    NONE = 0

class BreakOut(Enum):
  SUPPORT = 1
  RESISTENCE = 2
  NONE = 0

class Candle(Enum):
  GREEN = 1
  RED = 2
  BLACK = 0

class Trade(Enum):
  T1 = 1
  T2 = 2
  T3 = 3
  S1 = 4
  NO =0

class Signal(Enum):
  BUY = 0
  SELL = 1
  NONE = 2

class HammerCandleSys(Enum):
  Hammer = 1
  InvertedHammer = 2
  HangingMan = 3
  ShootingStar = 4
  NONE = 0

class StarCandleSys(Enum):
  MORNING = 1
  EVENING = 2
  NONE = 0

class DojiCandleSys(Enum):
  BULL = 1
  BEAR = 2
  NONE = 0

class MarubozuCandleSys(Enum):
  BULL = 1
  BEAR = 2
  NONE = 0

class HaramiCandleSys(Enum):
  BULL = 1
  BEAR = 2
  NONE = 0

class ThreeSystem_Method(Enum):
  BULL = 1
  BEAR = 2
  NONE = 0

class SR_First_Method(Enum):
  BUY_AT_SUPPORT = 1
  BUY_AT_RESISTENCE = 2
  SELL = 3
  NONE = 0

class Alert(Enum):
  SHORTFALL = 1
  NONE = 0