import yfinance as yf
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import datetime as dt


def download_data(stock, start, end):
    data= {}
    ticker = yf.download(stock, start, end)
    data['price'] = ticker['Adj Close']
    return pd.DataFrame(data)

if __name__ == '__main__':
    start = dt.datetime(2015, 1, 1)
    end = dt.datetime(2020, 12, 1)


    stock_data = download_data('IBM', start, end)

    stock_data['return'] = np.log(stock_data.price / stock_data.price.shift(1))
    stock_data['move'] = stock_data['price'] - stock_data['price'].shift(1)

    stock_data['up'] = np.where(stock_data['move'] > 0, stock_data['move'], 0)
    stock_data['down'] = np.where(stock_data['move'] < 0, stock_data['move'], 0)

    # RS
    stock_data['average_gain'] = stock_data['up'].rolling(14).mean()
    stock_data['average_loss'] = stock_data['down'].rolling(14).mean()
    RS = stock_data['average_gain'] / stock_data['average_loss']
    RSI = 100 - (100 / (1 + RS))

    stock_data['RSI'] = stock_data.dropna()

    print(stock_data)
    plt.plot(stock_data['rsi'])
    plt.show()


    print(stock_data)