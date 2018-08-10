import pandas as pd
import numpy as np
from stockdata import StockData
"""
Baseline strategy class will buy once at the beginning and sell at the end if the last price is better
"""
class Strategy:
    def __init__(self, stock_data):
        self.stock_data = stock_data
        self.actions = pd.DataFrame(index=self.stock_data.index, columns=['Stock', 'Action', 'Quantity'],
                                        dtype={'Stock': str, 'Action': str, 'Quantity': np.int})
        print('Strategy initialized.')

    def reset_data(self, stock_data):
        self.stock_data = stock_data

    def get_actions(self):
        print('Actions summary\n--------')
        self.actions.summarize(10)
        return self.actions

"""
Bollinger Band Strategy will buy an inital set of stocks. If any come up through the bottom band, buy.
 If anything goes down through the top band, sell
"""
class BollingerBandStrategy(Strategy):
    def __init__(self, stock_data=None):
        super(self, stock_data)

        print('Bollinger Band Strategy initialized.')

if __name__ == "__main__":
    symbols = ['SPY']
    start = '2016-11-01'
    end = '2017-11-01'
    dates = pd.date_range(start=start, end=end)
    stock_data = StockData(symbols, dates=dates)
    strategy = Strategy(stock_data)
    strategy.get_actions()
