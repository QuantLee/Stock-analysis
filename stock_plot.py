import pandas as pd
from pylab import *
from matplotlib.finance import candlestick_ohlc

style.use('ggplot')


def single_index_plot(df, index):
    plt.figure()
    df[index].plot()


def moving_average_plot(df):
    # a more complicated graph
    # calculate the moving average
    df['10moving average'] = df['Close'].rolling(window=10, min_periods=0).mean()
    df['30moving average'] = df['Close'].rolling(window=30, min_periods=0).mean()
    plt.figure()
    ax1 = plt.subplot2grid((10, 1), (0, 0), rowspan=5, colspan=1)
    ax2 = plt.subplot2grid((10, 1), (6, 0), rowspan=2, colspan=1, sharex=ax1)
    ax1.plot(df.index, df['Close'])
    ax1.plot(df.index, df['10moving average'])
    ax1.plot(df.index, df['30moving average'])
    ax2.bar(df.index, df['Volume'], color='green')


def OHLC(df):
    # shrink the size of the data by creating a new dataframe
    df_ohlc = df['Close'].resample('10D').ohlc()
    df_volume = df['Volume'].resample('10D').sum()
    # we want to convert the dates into matplotlib.dates version
    df_ohlc = df_ohlc.reset_index()
    df_ohlc['Date'] = df_ohlc['Date'].map(date2num)
    # figure setup
    plt.figure()
    ax1 = plt.subplot2grid((10, 1), (0, 0), rowspan=5, colspan=1)
    ax2 = plt.subplot2grid((10, 1), (6, 0), rowspan=2, colspan=1, sharex=ax1)
    ax1.xaxis_date()
    candlestick_ohlc(ax1, df_ohlc.values, width=2, colorup='g')
    ax2.fill_between(df_volume.index.map(date2num), df_volume.values, 0, color='blue')


def visualize_cor_table(stocks):
    df = pd.read_csv('sp500_joined_closes.csv')
    df = df[stocks]
    '''
        #choose number of stocks involved
        #df = df.ix[:,0:10]
        #choose several particular stock involve
        #df = df[['GOOG','MSFT','IBM','AAPL','FB','ORCL','AMZN']]
        '''
    # we can see the whole correlation table
    df_corr = df.corr()
    data1 = df_corr.values
    # build a correlation plot
    fig1 = plt.figure()
    ax1 = fig1.add_subplot(111)
    # red for negtive correlation and green for positive correlation and yellow for no corelation
    heatmap1 = ax1.pcolor(data1, cmap=cm.RdYlGn)
    fig1.colorbar(heatmap1)
    ax1.set_xticks(arange(data1.shape[1]) + 0.5, minor=False)
    ax1.set_yticks(arange(data1.shape[0]) + 0.5, minor=False)
    ax1.invert_yaxis()
    ax1.xaxis.tick_top()
    column_labels = df_corr.columns
    row_labels = df_corr.index
    ax1.set_xticklabels(column_labels)
    ax1.set_yticklabels(row_labels)
    #xticks(rotation = 90)
    heatmap1.set_clim(-1, 1)
    tight_layout()
    #plt.savefig('correlations.png', dpi = (300))
