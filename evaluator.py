class Evaluator:
    def __init__(self, evaluator_config=None, strategy=None, portfolio=None, portfolio_analyzer=None, stock_data=None):
        self.evaluator_config = evaluator_config
        self.strategy = strategy
        self.portfolio = portfolio
        self.portfolio_analyzer = portfolio_analyzer
        self.stock_data = stock_data
    def evaluate(self):
        return