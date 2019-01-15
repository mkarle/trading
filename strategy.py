import pandas as pd
import numpy as np
from stockdata import StockData
import transaction
from abc import ABCMeta, abstractmethod


'''
Baseline strategy class will buy once at the beginning and sell at the end
'''


class Strategy:
    def __init__(self):
        self.transactions = pd.DataFrame()
        print('Strategy initialized.')

    def get_transactions(self):
        return self.transactions

    def strategize(self, stock_data=None):
        print('Strategizing...')

        start_date = stock_data.dates[0]
        end_date = stock_data.dates[-1]
        self.transactions = transaction.initialize_actions(dates=[start_date, end_date], symbols=stock_data.symbols)

        self.transactions.loc[start_date, :] = stock_data.adj_close.loc[start_date, :]\
            .transform(lambda x: transaction.BuyTransaction(quantity=1, price=x))
        self.transactions.loc[end_date, :] = stock_data.adj_close.loc[end_date, :]\
            .transform(lambda x: transaction.SellTransaction(quantity=1, price=x))
        print('Finished strategizing')


'''
Bollinger Band Strategy will buy an inital set of stocks. If any come up through the bottom band, buy.
 If anything goes down through the top band, sell
'''


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
    actions = strategy.get_transactions()
    print('Actions sample\n--------')
    print(actions.head(10))
    print(actions.tail(10))

    bbs = BollingerBandStrategy()
