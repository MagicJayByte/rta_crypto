import pandas as pd
import numpy as np
import yfinance as yf
import datetime as dt
import matplotlib.pyplot as plt


class MovingAverageRSIStrategy:
    def __init__(self, capital, stock, start, end, short_period, long_period):
        self.capital = capital
        self.equity = [capital]
        self.stock = stock
        self.start = start
        self.end = end
        self.short_period = short_period
        self.long_period = long_period
        self.data = None
        self.is_long = False

    def download_data(self):
        data = {}
        ticker = yf.download(self.stock, self.start, self.end)
        data['price'] = ticker['Adj Close']
        self.data = pd.DataFrame(data)

    def plot_equity(self):
        print("Profit of the trading strategy: %0.2f%%" % (
                    (float(self.equity[-1]) - float(self.equity[0])) / float(self.equity[0]) * 100))
        print("Actual capital %0.2f%%" % self.equity[-1])
        plt.figure(figsize=(12, 6))
        plt.title('Equity Curve')
        plt.plot(self.equity, label='Stock Price', color='green')
        plt.xlabel('Date')
        plt.ylabel('Capital ($)')
        plt.show()

    def simulate(self):
        price_when_buy = 0

        for index, row in self.data.iterrows():
            if row['short_ma'] < row['long_ma'] and self.is_long:
                self.equity.append(row['price'] * self.capital / price_when_buy)
                self.is_long = False
                print("SELL")
            elif row['short_ma'] > row['long_ma'] and not self.is_long and row['rsi'] < 30:
                price_when_buy = row['price']
                self.is_long = True
                print("BUY")

    def construct_signals(self):
        self.data['short_ma'] = self.data['price'].ewm(span=self.short_period).mean()
        self.data['long_ma'] = self.data['price'].ewm(span=self.long_period).mean()
        self.data['move'] = self.data['price'] - self.data['price'].shift(1)
        self.data['up'] = np.where(self.data['move'] > 0, self.data['move'], 0)
        self.data['down'] = np.where(self.data['move'] < 0, self.data['move'], 0)
        self.data['average_gain'] = self.data['up'].rolling(14).mean()
        self.data['average_loss'] = self.data['down'].abs().rolling(14).mean()
        rs = self.data.average_gain / self.data.average_loss
        self.data['rsi'] = 100.0 - (100.0 / (1.0 + rs))
        self.data = self.data.dropna()

    def plot_signals(self):
        plt.figure(figsize=(12, 6))
        plt.plot(self.data['price'], label='Stock Price', color='black')
        plt.plot(self.data.short_ma, label='Short Moving Average', color='blue')
        plt.plot(self.data.long_ma, label='Long Moving Average', color='red')
        plt.title('Moving Average Strategy with RSI')
        plt.xlabel('Date')
        plt.ylabel('Stock Price')
        plt.show()


if __name__ == '__main__':
    start = dt.datetime(2015, 1, 1)
    end = dt.datetime(2020, 1, 1)

    model = MovingAverageRSIStrategy(100, 'IBM', start, end, 40, 150)
    model.download_data()
    model.construct_signals()
    model.plot_signals()
    model.simulate()
    model.plot_equity()
