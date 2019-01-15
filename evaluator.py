import utils
import datetime as dt
import pandas as pd
import matplotlib.pyplot as plt
from stockdata import StockData
from strategy import Strategy
import transaction
from copy import deepcopy


class Evaluator:
    def __init__(self, evaluator_config=None, strategy=None, portfolio=None, portfolio_analyzer=None, stock_data=None):
        self.evaluator_config = evaluator_config
        self.strategy = strategy
        self.portfolio = portfolio
        self.portfolio_analyzer = portfolio_analyzer
        self.stock_data = stock_data

    def evaluate(self, portfolio=None, ):
        portfolio
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
    evaluator = evaluator.Evaluator()
    print(evaluator.evaluate(portfolio))