import Learner
from sklearn.metrics import mean_squared_error
from sklearn.neighbors import KNeighborsRegressor


class KNNRegressionLearner:
    def __init__(self, k):
        self.regressor = KNeighborsRegressor(n_neighbors=k, algorithm='kd_tree', n_jobs=-1)

    def train(self, Xtrain, Ytrain):
        self.regressor.fit(Xtrain, Ytrain)
    def predict(self, X):
        return self.regressor.predict(X)
    def test(self, test_input, test_output):
        predictions = self.regressor.predict(test_input)
        return predictions, mean_squared_error(test_output, predictions)



'''
knn regression, the output is the value for the object

'''