import pandas as pd
import datetime
import pytz
import pandas_datareader.data as web


def get_stock_data(stock):
    '''
    Get stock data using Google API, the stock price is up to date, from 2012.
    save as csv file
    Example: Get_data_Print_tail()
    '''
    start = datetime.datetime(2012, 1, 1)
    end = datetime.datetime.now(pytz.timezone('America/New_York'))
    df = web.DataReader(stock, 'google', start, end)
    # save the DataFrame as a csv file in the present working directory
    df.to_csv('stock_csv/' + stock + '.csv')
    # then rather than reading the file from Yahoo Finance, we can read it from our csv
    df = pd.read_csv('stock_csv/' + stock + '.csv', parse_dates=True, index_col=0)
    # this DataFrame transfer is reversible
    print('Stock: ' + stock)
    return(df)
