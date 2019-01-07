'''import utils
import datetime as dt
import pandas as pd
import matplotlib.pyplot as plt
import learning.KNNRegressionLearner as knnlearner
from stockdata import StockData

if __name__ == "__main__":
    symbols = ['SPY']
    stock_data = StockData(symbols)
    Xtrain, Ytrain = stock_data.get_training_data()
    learner = knnlearner.KNNRegressionLearner(5)
    print(Xtrain.shape)
    print(Ytrain.shape)
    learner.train(Xtrain.values, Ytrain.values)

    Xtest, Ytest = stock_data.get_test_data()
    print(Xtest.shape)
    print(Ytest.shape)
    print(stock_data.adj_close.shape)
    print(stock_data.features.shape)
    predictions, accuracy = learner.test(Xtest.values, Ytest.values)
    print(accuracy)

    ax = Ytest.plot()
    plt.plot(Ytest.index.values, predictions)
    plt.show()


'''