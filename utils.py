import os
import pandas as pd
import pandas_datareader.data as web
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import minimize
import datetime as dt

SHARPE_RATIO_CONSTANT = np.sqrt(252)
start = '2017-11-01'
end = dt.date.today().isoformat()
dates = pd.date_range(start, end)

def save_data_to_csv(symbol):
	web.DataReader(symbol, 'yahoo', start, end).to_csv('data/' + symbol + '.csv')

def symbol_to_path(symbol, base_dir="data"):
	return os.path.join(base_dir, "{}.csv".format(str(symbol)))

def read_data(symbol):
	try:
		return pd.read_csv(symbol_to_path(symbol), index_col='Date', parse_dates=True, usecols=['Date', 'Adj Close'], na_values=['nan'])
	except IOError:
		save_data_to_csv(symbol)
		return read_data(symbol)

def get_adjusted_close(symbols, dates=dates):
	df = pd.DataFrame(index=dates)
	if 'SPY' not in symbols:
		symbols.insert(0, 'SPY')

	for symbol in symbols:
		dftemp = read_data(symbol).rename(columns={'Adj Close':symbol})
		df = df.join(dftemp, how='inner')
		if symbol == 'SPY':
			df = df.dropna(subset=['SPY'])
	return df

def normalize(df):
	return df / df.ix[0,:]

def get_bollinger_bands(rm, rstd):
	upper = rm + rstd * 2
	lower = rm - rstd * 2
	return upper, lower

def get_daily_returns(df):
	dr = df.copy()
	dr.ix[1:] = df/df.shift(1) - 1
	if len(dr.axes) == 1:
		dr.ix[0] = 0
	else:
		dr.ix[0,:] = 0
	return dr

def get_cumulative_returns(df):
	return normalize(df) - 1

def get_sharpe_ratio(daily_returns, daily_risk_free = 0):
	return SHARPE_RATIO_CONSTANT * (daily_returns - daily_risk_free).mean() / daily_returns.std()

def get_volatility(df):
	return df.std()

def get_rolling_std(df, window):
	return df.rolling(window=window, center=False).std()

def get_rolling_average(df, window):
	return df.rolling(window=window, center=False).mean()

def port_objective(allocs, normed,start_val):
	alloced = normed * allocs
	pos_vals = alloced * start_val
	port_val = pos_vals.sum(axis=1)
	daily_returns = get_daily_returns(port_val)
	daily_returns = daily_returns.ix[1:]
	return (-get_sharpe_ratio(daily_returns))

def optimize(symbols, start_val, dates=dates):
	allocs = [1. / len(symbols) for x in symbols]

	prices = get_adjusted_close(symbols)
	normed = normalize(prices)

	constraints = {'type':'eq', 'fun':lambda x: sum(x) == 1}
	return minimize(port_objective, x0=allocs, args=(normed,start_val), method='SLSQP', bounds=[(0,1) for x in symbols], constraints=constraints)

def get_beta(daily_returns, symbol):
	beta, alpha = np.polyfit(daily_returns['SPY'], daily_returns[symbol], 1)
	return beta

def test_run():

	symbols = [ 'SPY','AMZN', 'GOOG']

	df = get_adjusted_close(symbols, dates)
	#print df.ix['2010-01-01':'2010-01-31']
	#print df['GOOG']
	#print df[['IBM', 'GLD']]
	#print df.ix['2010-03-10':'2010-03-15', 	['SPY', 'IBM']]
	#ax = df.plot()

	#print df.mean()
	#print df.std()
	#rm = pd.rolling_mean(df, window=20)
	#rstd = pd.rolling_std(df, window=20)
	#upper, lower = get_bollinger_bands(rm, rstd)
	daily_returns = get_daily_returns(df)
	#ax = rm.plot(label='rolling_mean', ax=ax)
	#ax = upper.plot(label='upper', ax=ax)
	#ax = lower.plot(label='lower', ax=ax)
	#plt.show()
	#daily_returns.plot(label="daily_returns")
	#plt.show()

	#cr = get_cumulative_returns(df)
	#cr.plot(label='cr')
	#plt.show()

	#daily_returns['SPY'].hist(bins=20,label='SPY')
	#daily_returns['AMZN'].hist(bins=20, label='AMZN')
	#mean = daily_returns['SPY'].mean()
	#std = daily_returns['AMZN'].std()

	#plt.axvline(mean,color='w', linestyle='dashed', linewidth=2)
	#plt.axvline(std,color='r', linestyle='dashed', linewidth=2)
	#plt.axvline(-std,color='r', linestyle='dashed', linewidth=2)

	daily_returns.plot(kind='scatter', x='AMZN', y='SPY')
	beta_AMZN, alpha_AMZN = np.polyfit(daily_returns['SPY'], daily_returns['AMZN'],1)
	beta_GOOG, alpha_GOOG = np.polyfit(daily_returns['SPY'], daily_returns['GOOG'],1)
	plt.plot(daily_returns['SPY'],beta_AMZN * daily_returns['SPY'] + alpha_AMZN, '-', color='r')
	plt.show()
	print daily_returns.corr(method='pearson')
	#daily_returns.plot(kind='scatter', x='GOOG', y='SPY')
	#plt.show()
	print daily_returns.kurtosis()

if __name__ == "__main__":
	test_run()