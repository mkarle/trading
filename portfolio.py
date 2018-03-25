import utils
import datetime as dt
import pandas as pd
import matplotlib.pyplot as plt
if __name__ == "__main__":
	start_val = 1000000
	symbols = ['VV', 'VUG', 'VFH', 'VOO', 'VGT', 'SPY']
	print(utils.optimize(symbols, start_val))

	