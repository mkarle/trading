import utils
import datetime as dt
import pandas as pd

class StockData:
    start = '2016-11-01'
    end = dt.date.today().isoformat()
    dates = pd.date_range(start, end)
    def __init__(self, symbols, dates=dates, windows=20, days_ahead=5):
        self.symbols = symbols
        if 'SPY' not in self.symbols:
            self.symbols.insert(0, 'SPY')
        self.dates = dates
        self.windows = windows
        self.days_ahead = days_ahead
        self.adj_close = utils.get_adjusted_close(self.symbols, self.dates)
        self.normalized_adj_close = utils.normalize(self.adj_close)
        self.daily_returns = utils.get_daily_returns(self.adj_close)
        self.simple_moving_average = utils.get_rolling_average(self.adj_close, windows)
        self.simple_moving_std = utils.get_rolling_std(self.adj_close, windows)
        self.bollinger_bands = utils.get_bollinger_bands(self.simple_moving_average, self.simple_moving_std)
        self.cumulative_returns = utils.get_cumulative_returns(self.adj_close)
        self.volatility = utils.get_volatility(self.adj_close)
        # self.beta = utils.get_beta(self.daily_returns)
        # self.features = self.get_features()
        #self.outputs = self.adj_close.copy(deep=True)
        #print(self.features.shape)
        #print(self.outputs.shape)

'''
    def get_training_data(self):
        shape = self.features.shape
        Xtrain = self.features[: 2*shape[0]/3]
        Ytrain = self.outputs[: 2*shape[0]/3]
        return Xtrain, Ytrain

    def get_test_data(self):
        length = self.features.shape[0]
        Xtest = self.features[-length/3: length-self.days_ahead]
        Ytest = self.outputs[-length/3: length-self.days_ahead]
        return Xtest, Ytest

    def get_features(self):
        d = {'SMA %': (self.adj_close / self.simple_moving_average).stack(),
             'Volatility': self.simple_moving_std.stack()}
        features = pd.DataFrame(d)
        return features

'''