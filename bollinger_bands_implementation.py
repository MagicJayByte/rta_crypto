import backtrader as bt
import datetime as dt
import pandas as pd
import yfinance as yf



def download_data(stock, start, end):
    data = yf.download(stock, start, end)
    return pd.DataFrame(data)


class BollingerBandsStrategy(bt.Strategy):

    params = (
        ('period', 20),
        ('std', 2),
        ('size', 20)
    )

    def __init__(self):
        self.bollinger = bt.indicators.BollingerBands(period=self.p.period,
                                                      devfactor = self.p.std)
        
    def next(self):

        #if we do not have any open positions
        if not self.position:
            # open short position
            if self.data.close > self.bollinger.top:
                self.sell(size=self.p.size)
            #open long positions if needed
            if self.data.close[0] < self.bollinger.lines.bot:
                self.buy(size=self.p.size)
        else:
            #We have opened long positions. We have to check whether to close the long position
            if self.position.size > 0:
                # close it when the price crosses the middle line
                self.sell(exectype=bt.Order.Limit, price=self.bollinger.lines.mid[0],
                          size=self.p.size)
            #close the short position (with the help of buy)
            else:
                # we have an open short position - close it as well
                self.buy(exectype=bt.Order.Limit, price=self.bollinger.lines.mid[0],
                         size=self.p.size)
    
if __name__ == "__main__":
    
    start_date = dt.datetime(2010, 1, 1)
    end_date = dt.datetime(2019, 1, 1)

    cerebro = bt.Cerebro()
    cerebro.addstrategy(BollingerBandsStrategy)

    data_yf = download_data('IBM', start_date, end_date)
    data = bt.feeds.PandasData(dataname = data_yf)
    cerebro.adddata(data)
    cerebro.addobserver(bt.observers.Value)
    cerebro.addanalyzer(bt.analyzers.SharpeRatio, riskfreerate=0.0)
    cerebro.addanalyzer(bt.analyzers.Returns)
    cerebro.addanalyzer(bt.analyzers.DrawDown)

    print('Initial Capital: $%.2f' % cerebro.broker.getvalue())
    
    results = cerebro.run()

    print(f"Sharpe: {results[0].analyzers.sharperatio.get_analysis()['sharperatio']:.3f}")
    print(f"Annual Return: {results[0].analyzers.returns.get_analysis()['rnorm100']:.2f}%")
    print(f"Max Drawdown: {results[0].analyzers.drawdown.get_analysis()['max']['drawdown']:.2f}%")
    print('Capital: $%.2f' % cerebro.broker.getvalue())
    