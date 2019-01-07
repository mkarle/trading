class Evaluator:
    def __init__(self, evaluator_config=None, strategy=None, portfolio=None, portfolio_analyzer=None, stock_data=None):
        self.evaluator_config = evaluator_config
        self.strategy = strategy
        self.portfolio = portfolio
        self.portfolio_analyzer = portfolio_analyzer
        self.stock_data = stock_data
    def evaluate(self):
        return

if __name__ == "__main__":
    symbols = ['SPY']
    start = '2016-11-01'
    end = '2017-11-01'
    dates = pd.date_range(start=start, end=end)
    stock_data = StockData(symbols, dates=dates)

    strategy = Strategy(stock_data)
    actions = strategy.get_actions()
    print('Actions sample\n--------')
    print(actions.head(10))
    print(actions.sample(10))
    print(actions.tail(10))

    strategy.strategize()
    actions = strategy.get_actions()
    print('Actions sample\n--------')
    print(actions.head(10))
    print(actions.sample(10))
    print(actions.tail(10))