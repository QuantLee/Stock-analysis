import pandas as pd
import pickle
import datetime
import os
import pandas as pd
import pandas_datareader.data as web
import pytz
import time
import save_tickers


# define start time and end time(change of time: datetime.timedelta(days=1))
start = datetime.datetime(2016, 1, 1)
end = datetime.datetime.now(pytz.timezone('America/New_York'))


def get_data(reload_sp500=False):
    '''
        the default input of reload_sp500 is False. If it is true, all tickers will be renewed.
    '''
    # renew the database, delete all stock files
    # filelist = [f for f in os.listdir("./stock_dfs") if f.endswith(".csv")]
    # for f in filelist:
    #     os.remove("./stock_dfs/{}".format(f))

    if reload_sp500:
        tickers = save_tickers.save_sp500_tickers()
    else:
        with open("sp500tickers.pickle", "rb") as f:
            tickers = pickle.load(f)

    if not os.path.exists('stock_dfs'):
        os.makedirs('stock_dfs')

    for ticker in tickers:
        # just in case your connection breaks, we'd like to save our progress!
        if not os.path.exists('stock_dfs/{}.csv'.format(ticker)):
            # because now the wikipedia is using '.' instead of '-', sometimes just use . to replace -.
            try:
                df = web.DataReader(ticker, "google", start, end)
                df.to_csv('stock_dfs/{}.csv'.format(ticker))
            except Exception as e:
                print('ticker error: {}'.format(ticker))
        else:
            print('Already have {}'.format(ticker))


def Close_price_compile():
    '''
    compile all data into one csv sheet.
    '''
    # update
    if os.path.exists('sp500_joined_closes.csv'):
        os.remove('sp500_joined_closes.csv')

    with open("sp500tickers.pickle", "rb") as f:
        tickers = pickle.load(f)

    # there might be tickers that the web can not reach
    tickers = [t for t in tickers if os.path.exists('stock_dfs/{}.csv'.format(t))]

    main_df = pd.DataFrame()

    for count, ticker in enumerate(tickers):
        df = pd.read_csv('stock_dfs/{}.csv'.format(ticker))
        df.set_index('Date', inplace=True)

        df.rename(columns={'Close': ticker}, inplace=True)
        df.drop(['Open', 'High', 'Low', 'Volume'], 1, inplace=True)

        if main_df.empty:
            main_df = df
        else:
            main_df = main_df.join(df, how='outer')
    main_df.dropna()
    print(main_df.head())
    main_df.to_csv('sp500_joined_closes.csv')


def Rate_return_compile():
    '''
    compile all data into one csv sheet.
    '''
    # update
    if os.path.exists('sp500_joined_rates.csv'):
        os.remove('sp500_joined_rates.csv')

    with open("sp500tickers.pickle", "rb") as f:
        tickers = pickle.load(f)

    # there might be tickers that the web can not reach
    tickers = [t for t in tickers if os.path.exists('stock_dfs/{}.csv'.format(t))]

    main_df = pd.DataFrame()

    for count, ticker in enumerate(tickers):
        df = pd.read_csv('stock_dfs/{}.csv'.format(ticker))
        df.set_index('Date', inplace=True)

        df.rename(columns={'Close': ticker}, inplace=True)
        df.drop(['Open', 'High', 'Low', 'Volume'], 1, inplace=True)

        if main_df.empty:
            main_df = df.shift(1) / df - 1
        else:
            main_df = main_df.join(df.shift(1) / df - 1, how='outer')
    main_df.dropna()
    print(main_df.head(10))
    main_df.to_csv('sp500_joined_rates.csv')
    return main_df


def compile_newest_OHLCV():
    '''
    get the newest open high low close volume data
    '''
    with open("sp500tickers.pickle", "rb") as f:
        tickers = pickle.load(f)
    # there might be tickers that the web can not reach
    tickers = [t for t in tickers if os.path.exists('stock_dfs/{}.csv'.format(t))]

    main_df = pd.DataFrame()
    for count, ticker in enumerate(tickers):
        df = pd.read_csv('stock_dfs/{}.csv'.format(ticker))
        df = df.tail(1)
        df['stock'] = ticker

        if main_df.empty:
            main_df = df
        else:
            main_df = main_df.append(df, ignore_index=True)
    main_df = main_df.set_index(['stock'])
    print(main_df.head())
    main_df.to_csv('sp500_new_OHLCV.csv')
