import pandas as pd
import numpy as np
from stockdata import StockData


class Action:
    EMPTY = '---'
    HOLD = 'HOLD'
    BUY = 'BUY'
    SELL = 'SELL'
    ACTIONS = [EMPTY, HOLD, BUY, SELL]

"""
Baseline strategy class will buy once at the beginning and sell at the end
"""
class Strategy:
    def __init__(self):
        self.actions = pd.DataFrame()
        print('Strategy initialized.')

    def get_actions(self):
        return self.actions

    def strategize(self, portfolio=None, stock_data=None):
        print('Strategizing...')
        index = pd.MultiIndex.from_product([stock_data.dates, stock_data.symbols], names=['Date', 'Stock'])
        size = index.size
        action_series = pd.Series([Action.EMPTY] * size, index=index,
                                  dtype=pd.api.types.CategoricalDtype(categories=Action.ACTIONS))
        quantity_series = pd.Series([0] * size, index=index, dtype='int')

        self.actions = pd.DataFrame(data={'Action': action_series, 'Quantity': quantity_series})
        start_date = self.actions.index[0][0]
        end_date = self.actions.index[-1][0]
        self.actions['Action'] = [Action.HOLD] * self.actions['Action'].size
        self.actions.loc[(start_date, ), 'Action'] = [Action.BUY] * self.actions.loc[(start_date, ), 'Action'].size
        self.actions.loc[(end_date, ), 'Action'] = [Action.SELL] * self.actions.loc[(end_date, ), 'Action'].size
        self.actions['Quantity'] = [1]*self.actions['Quantity'].size
        print('Finished strategizing')


"""
Bollinger Band Strategy will buy an inital set of stocks. If any come up through the bottom band, buy.
 If anything goes down through the top band, sell
"""
class BollingerBandStrategy(Strategy):
    def __init__(self):
        super().__init__()

        print('Bollinger Band Strategy initialized.')


if __name__ == "__main__":
    symbols = ['SPY']
    start = '2016-11-01'
    end = '2017-11-01'
    dates = pd.date_range(start=start, end=end)
    stock_data = StockData(symbols, dates=dates)

    strategy = Strategy()

    strategy.strategize(stock_data=stock_data)
    actions = strategy.get_actions()
    print('Actions sample\n--------')
    print(actions.head(10))
    print(actions.tail(10))

    bbs = BollingerBandStrategy()
