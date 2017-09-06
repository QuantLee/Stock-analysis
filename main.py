import os
import get_stock_data as gd
import stock_plot as sp
import pickle
import matplotlib.pyplot as plt
import get_market_data as gmd

# update the database and joined close price
'''
# gmd.get_data(reload_sp500=False)
# gmd.Close_price_compile()
# get single stock date and visualize it
# df = gd.get_stock_data('GOOGL')
# sp.single_index_plot(df, 'Close')
# sp.moving_average_plot(df)
# sp.OHLC(df)
# plt.show()
# visualize the correlation table of selected stock based on the closed price
# stocks = ['GOOG', 'MSFT', 'IBM', 'AAPL', 'FB', 'ORCL', 'AMZN']
# sp.visualize_cor_table(stocks)
# plt.show()
'''


# compile the data and tickers
data = gmd.Rate_return_compile()
with open("sp500tickers.pickle", "rb") as f:
    tickers = pickle.load(f)
# there might be tickers that the web can not reach
tickers = [t for t in tickers if os.path.exists('stock_dfs/{}.csv'.format(t))]

data = data[1:, :]
print(data.head())
