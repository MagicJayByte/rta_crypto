import yfinance as yf
import matplotlib.pyplot as plt
import datetime as dt
import pandas as pd

def download_data(stock, start, end):
    data = yf.download(stock, start, end)
    return pd.DataFrame(data)


if __name__ == '__main__':
    start_date = dt.datetime(2011, 1, 1)
    end_date = dt.datetime(2012, 1, 1)

    # Calculate the Bollinger bands
    stock_data = download_data('IBM', start_date, end_date)
    stock_data['tp'] = (stock_data['Close'] + stock_data['Low'] + stock_data['High']) / 3
    stock_data['std'] = stock_data['tp'].rolling(20).std()
    stock_data['ma'] = stock_data['tp'].rolling(20).mean()
    stock_data['upper_band'] = stock_data['ma'] + 2 * stock_data['std']
    stock_data['lower_band'] = stock_data['ma'] - 2 * stock_data['std']
    stock_data = stock_data.dropna()
    plt.plot(stock_data['Close'])
    plt.plot(stock_data['upper_band'], color = 'orange')
    plt.plot(stock_data['lower_band'], color = 'purple')
    plt.fill_between(stock_data.index, stock_data['upper_band'],
                     stock_data['lower_band'], facecolor = 'orange', alpha=0.1)
    plt.title('Boliinger Bands')
    plt.xlabel('Date')
    plt.ylabel('Stock Price')
    plt.show()
    print(stock_data)