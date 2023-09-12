#https://docs.python.org/3/library/unittest.html

import unittest
import Finder.Pattern as pattern
import Finder.CandleStick as candle
import Enum.MarketEnum as mEnum
import Utility.NSEIndia.NSEAPI as nseAPI

class TestPatternMethods(unittest.TestCase):
    def setUp(self):
         self._nseAPI = nseAPI.NSEAPI()

    def test_findExtremeReversalPattern(self):
        result = pattern.findExtremeReversalPattern(25, 30, 20, 22, 20, 30, 10, 71, 1)
        self.assertEqual(result, mEnum.MarketType.BEARISH)

    def test_findExtremeReversalPattern(self):
        result = pattern.findEngulfingPattern(10, 40, 20, 22, 20, 21, 21, 71, 9.8)
        self.assertEqual(result, mEnum.MarketType.BULLISH)

    def test_findDojiReversalPattern_Bearish(self):
        prev_open = 15
        prev_high = 21
        prev_low = 9
        prev_close = 15.5
        prev2_open = 15
        prev2_high = 21
        prev2_low = 9
        prev2_close = 15.5
        open = 15
        high = 21
        low = 9
        close = 8
        avgPrevCandleSize = 12.5
        sma10 = 8
        result = pattern.findDojiReversalPattern(open, high, low, close, prev_open, prev_high, prev_low, prev_close, prev2_open, prev2_high, prev2_low, prev2_close, avgPrevCandleSize, sma10)
        self.assertEqual(result, mEnum.MarketType.BEARISH)

    def test_findDojiReversalPattern_Bearish_2ndAttempt(self):
        prev_open = 15
        prev_high = 15
        prev_low = 9
        prev_close = 9
        prev2_open = 15
        prev2_high = 21
        prev2_low = 9
        prev2_close = 15.5
        open = 15
        high = 21
        low = 9
        close = 8
        avgPrevCandleSize = 12.5
        sma10 = 8
        result = pattern.findDojiReversalPattern(open, high, low, close, prev_open, prev_high, prev_low, prev_close, prev2_open, prev2_high, prev2_low, prev2_close, avgPrevCandleSize, sma10)
        self.assertEqual(result, mEnum.MarketType.BEARISH)

    def test_findDojiReversalPattern_Bullish(self):
        prev_open = 15
        prev_high = 7.9
        prev_low = 21
        prev_close = 15.5
        prev2_open = 15
        prev2_high = 21
        prev2_low = 9
        prev2_close = 15.5
        open = 15
        high = 21
        low = 9
        close = 8
        avgPrevCandleSize = 13.5
        sma10 = 22
        result = pattern.findDojiReversalPattern(open, high, low, close, prev_open, prev_high, prev_low, prev_close, prev2_open, prev2_high, prev2_low, prev2_close, avgPrevCandleSize, sma10)
        self.assertEqual(result, mEnum.MarketType.BULLISH)

    def test_findDojiReversalPattern_Bullish_2ndAttempt(self):
        prev_open = 15
        prev_high = 21
        prev_low = 14
        prev_close = 21
        prev2_open = 15
        prev2_high = 7.9
        prev2_low = 21
        prev2_close = 15.5
        open = 15
        high = 21
        low = 9
        close = 8
        avgPrevCandleSize = 13.5
        sma10 = 22
        result = pattern.findDojiReversalPattern(open, high, low, close, prev_open, prev_high, prev_low, prev_close, prev2_open, prev2_high, prev2_low, prev2_close, avgPrevCandleSize, sma10)
        self.assertEqual(result, mEnum.MarketType.BULLISH)

    def test_findDojiCandle_Valid(self):
        open = 15
        high = 21
        low = 9
        close = 15.5
        bodyWidthPercent = 10

        result = candle.find_Doji(open, high, low, close, bodyWidthPercent)
        self.assertEqual(result, True)

    def test_check_nseAPI(self):
        data = self._nseAPI.get_historic_data()
        self.assertIsNotNone(data, True)


if __name__ == '__main__':
    unittest.main()