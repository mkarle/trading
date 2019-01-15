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
    CASH = "_CASH"

    def __init__(self, initial_investment=0, symbols=None, stock_data=None, dates=None):
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
        self.allocations = pd.DataFrame(index=stock_data.dates, columns=columns).fillna(
            value=0
        )

    def _init_without_stock_data(self, symbols, dates):
        columns = ["SPY"] if symbols is None else deepcopy(symbols)
        columns.extend([Portfolio.CASH])
        dates = (
            pd.date_range(start=dt.date.today().isoformat(), period=1)
            if dates is None
            else dates
        )
        self.allocations = pd.DataFrame(index=dates, columns=columns).fillna(value=0)

    def optimize(self, strategy=None, stock_data=None):
        assert strategy is not None, "Give me a real strategy."

        strategy.strategize(stock_data=stock_data)
        self._apply_transactions(strategy.get_transactions())

    def _apply_transactions(self, transactions):
        def transactions_to_quantity_and_price_changes(row):
            new_row = row.map(lambda transaction: transaction.get_effect_on_quantity())
            new_row["_CASH"] = row.map(
                lambda transaction: transaction.get_total_price()
            ).sum()
            return new_row

        changes = (
            transactions.apply(transactions_to_quantity_and_price_changes, axis=1)
            .cumsum()
            .resample("1D")
            .ffill()
        )
        self.allocations = self.allocations.add(changes, fill_value=None).dropna()


class PortfolioAnalyzer:
    CLOSING_VALUE = "_C_VAL"

    def __init__(self, portfolio=None, stock_data=None):
        self.portfolio = portfolio
        self.stock_data = stock_data
        self.portfolio_value = None
        self._calculate_portfolio_value()
        self.get_portfolio_value()

    def get_portfolio_value(self):
        if self.portfolio_value is None:
            self._calculate_portfolio_value()
        return self.portfolio_value

    def _calculate_portfolio_value(self):
        data = (
            self.portfolio.allocations.loc[:, self.portfolio.allocations.columns != Portfolio.CASH]
            .mul(self.stock_data.adj_close, fill_value=None)
            .ffill()
            .sum(axis="columns")
            .add(self.portfolio.allocations[Portfolio.CASH], fill_value=None)
            .ffill()
        )

        self.portfolio_value = pd.DataFrame(data=data, columns=[self.CLOSING_VALUE])


if __name__ == "__main__":
    symbols = ["SPY", "AMZN"]
    start = "2016-11-01"
    end = "2017-11-01"
    dates = pd.date_range(start=start, end=end)
    stock_data = StockData(symbols, dates=dates)

    strategy = Strategy()
    portfolio = Portfolio(symbols=symbols, stock_data=stock_data, dates=dates)
    portfolio.optimize(strategy=strategy, stock_data=stock_data)

    portfolio_analyzer = PortfolioAnalyzer(portfolio=portfolio, stock_data=stock_data)
