import utils
import datetime as dt
import pandas as pd
import matplotlib.pyplot as plt


class Portfolio:
    CASH = '_CASH'
    CLOSING_VALUE = '_C_VALUE'

    def __init__(self, initial_investment=1000, symbols=None, stock_data=None, dates=None):
        self.initial_investment = initial_investment
        self.cash = initial_investment
        if stock_data is not None:
            self._init_with_stock_data(stock_data)
        else:
            self._init_without_stock_data(symbols, dates)
        self.allocations_df[[Portfolio.CASH, Portfolio.CLOSING_VALUE]] = self.cash

    def _init_with_stock_data(self, stock_data):
        columns = stock_data.symbols
        columns.extend([Portfolio.CASH, Portfolio.CLOSING_VALUE])
        self.allocations_df = pd.DataFrame(index=stock_data.dates, columns=columns).fillna(value=0)

    def _init_without_stock_data(self, symbols, dates):
        columns = ['SPY'] if symbols is None else symbols
        columns.extend([Portfolio.CASH, Portfolio.CLOSING_VALUE])
        dates = pd.date_range(start=dt.date.today().isoformat(), period=1) if dates is None else dates
        self.allocations_df = pd.DataFrame(index=dates, columns=columns).fillna(value=0)

