import Learner
class LinearModelLearner(Learner):
    def __init__(self):
        super(self)
        self.Xtrain = None
        self.Ytrain = None

        self.x_train_placeholder = None
        self.y_train_placeholder = None
        self.x_test_placeholder = None

    def train(self, Xtrain, Ytrain):
        self.Xtrain = Xtrain
        self.Ytrain = Ytrain