from backtesting import Backtest, Strategy
from backtesting.lib import crossover

from backtesting.test import SMA, GOOG

import talib


class smaCross(Strategy):
    def init(self):
        price = self.data.Close
        self.ma1 = self.I(talib.EMA, price, 8)
        self.ma2 = self.I(talib.EMA, price, 13)
        self.ma3 = self.I(talib.EMA, price, 21)
        self.ma4 = self.I(talib.EMA, price, 55)
        self.pos = False

    def next(self):
        if (self.ma1 > self.ma4) and (self.ma2 > self.ma4) and (self.ma3 > self.ma4):
            if self.pos == False:
                self.buy()
                self.pos = True
        elif (self.ma1 < self.ma4) and (self.ma2 < self.ma4) and (self.ma3 < self.ma4):
            if self.pos == True:
                self.sell()
                self.pos = False


bt = Backtest(GOOG, smaCross, commission=0.002, exclusive_orders=True)
stats = bt.run()
bt.plot()
