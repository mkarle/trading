import utils
import datetime as dt
import pandas as pd
import matplotlib.pyplot as plt
from stockdata import StockData
from strategy import Strategy
import transaction
from copy import deepcopy


def func(x):
    print(x)


class Portfolio:
    CASH = '_CASH'

    def __init__(self, initial_investment=1000, symbols=None, stock_data=None, dates=None):
        self.initial_investment = initial_investment
        self.cash = initial_investment
        if stock_data is not None:
            self._init_with_stock_data(stock_data)
        else:
            self._init_without_stock_data(symbols, dates)
        self.allocations[[Portfolio.CASH]] = self.cash

    def _init_with_stock_data(self, stock_data):
        columns = deepcopy(stock_data.symbols)
        columns.extend([Portfolio.CASH])
        self.allocations = pd.DataFrame(index=stock_data.dates, columns=columns).fillna(value=0)

    def _init_without_stock_data(self, symbols, dates):
        columns = ['SPY'] if symbols is None else deepcopy(symbols)
        columns.extend([Portfolio.CASH])
        dates = pd.date_range(start=dt.date.today().isoformat(), period=1) if dates is None else dates
        self.allocations = pd.DataFrame(index=dates, columns=columns).fillna(value=0)

    def optimize(self, strategy=None, stock_data=None):
        assert strategy is not None, "Give me a real strategy."

        strategy.strategize(portfolio=self, stock_data=stock_data)
        self._apply_transactions(strategy.get_transactions())

    def _apply_transactions(self, transactions):
        print(transactions.head(5))
        return


if __name__ == "__main__":
    symbols = ['SPY', 'AMZN']
    start = '2016-11-01'
    end = '2017-11-01'
    dates = pd.date_range(start=start, end=end)
    stock_data = StockData(symbols, dates=dates)

    strategy = Strategy()
    portfolio = Portfolio(symbols=symbols, stock_data=stock_data, dates=dates)
    portfolio.optimize(strategy=strategy, stock_data=stock_data)
