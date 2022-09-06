from enum import Enum

class ExportFrom(Enum):
  EXCEL = 1
  JSON = 2
  NONE = 0 

class InLine(Enum):
  SUPPORT = 1
  RESISTENCE = 2
  NONE = 0

class Trend(Enum):
  UP = 1
  DOWN = 2
  STRAIGHT = 3
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
  NONE = 0

class Trade(Enum):
  T1 = 1
  T2 = 2
  T3 = 3
  NO =0