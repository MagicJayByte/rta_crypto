import yfinance
import datetime as dt
import pandas as pd
from matplotlib import pyplot as plt


class MovingAverageCrossover:

    def __init__(self, capital, stock, start, end, short_period, long_period):
        self.data = None
        self.is_long = False
        self.capital = capital
        self.equity = [capital]
        self.stock = stock
        self.start = start
        self.end = end
        self.short_period = short_period
        self.long_period = long_period
        self.end = end

    def get_data(self):
        return self.data
    def get_equity(self):
        return self.equity
    def download_data(self):
        stock_data = {}
        ticker = yfinance.download(self.stock, self.start, self.end)
        stock_data['price'] = ticker['Adj Close']
        self.data = pd.DataFrame(stock_data)
    def construct_signals_simple(self):
        self.data['Short SMA'] = self.data['price'].rolling(window=self.short_period).mean()
        self.data['Long SMA'] = self.data['price'].rolling(window=self.long_period).mean()
        return self.data

    def construct_signals_exp(self):
        self.data['short_ema'] = self.data['price'].ewm(span=self.short_period).mean()
        self.data['long_ema'] = self.data['price'].ewm(span=self.long_period).mean()

    def plot_signals(self):
        plt.figure(figsize=(12, 6))
        plt.plot(self.data.price, label='Stock Price', color='blue')
        plt.plot(self.data['short_ema'], label='Short EMA', color='purple')
        plt.plot(self.data['long_ema'], label='Long EMA', color='red')
        plt.title('Moving Average (EMA) Crossover')
        plt.show()

    def simulate(self):

        price_when_buy = 0
        for index, row in self.data.iterrows():
            if row['short_ema'] < row['long_ema'] and self.is_long:
                self.equity.append(self.capital * row['price'] / price_when_buy)
                self.is_long = False
                print('SELL')
            elif row['short_ema'] > row['long_ema'] and not self.is_long:
                price_when_buy = row['price']
                self.is_long = True
                print('BUY')

    def plot_equity(self):
        print("Profit of the trading strategy: %.2f%%" % ((float((self.equity[-1]) - float(self.equity[0]))/float(self.equity[0]) * 100)))
        print("Actual capital: %.2f" % self.equity[-1])
        plt.figure(figsize=(12, 6))
        plt.title('Equity Curve')
        plt.plot(self.equity, label='Stock Price', color='blue')
        plt.xlabel('Date')
        plt.ylabel('Actual Capital $')
        plt.show()




if __name__ == '__main__':
    start_date = dt.datetime(2010,1,1)
    end_date = dt.datetime(2020, 1, 1)

    strategy = MovingAverageCrossover(100, 'MS', start_date, end_date, 30, 300)
    strategy.download_data()
    strategy.construct_signals_exp()
    strategy.plot_signals()
    strategy.simulate()
    strategy.plot_equity()