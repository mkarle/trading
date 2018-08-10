import utils
import datetime as dt
import pandas as pd
import matplotlib.pyplot as plt


class Portfolio:
    def __init__(self, initial_investment=100000):
        self.initial_investment = initial_investment
