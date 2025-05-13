import backtrader as bt
from datetime import datetime as dt
import yfinance as yf
import pandas as pd

class MovingAverageStrategy(bt.Strategy):


    params = (('period_fast',30), ('period_slow', 200),)

    def __init__(self):
        self.close_data = self.data.close
        self.fast_sma = bt.indicators.MovingAverageSimple(self.close_data, 
                                                          period=self.params.period_fast)
        self.slow_sma = bt.indicators.MovingAverageSimple(self.close_data, 
                                                          period=self.params.period_slow)
    def next(self):
        if not self.position:
            if self.fast_sma[0] > self.slow_sma[0] and self.fast_sma[-1] < self.slow_sma[-1]:
                print('BUY')
                self.buy()
        else:
            #check whether to close the position or not
            if self.fast_sma[0] < self.slow_sma[0] and self.fast_sma[-1] > self.slow_sma[-1]:
                print("CLOSE")
                self.close()
if __name__ == "__main__":
    cerebro = bt.Cerebro()
    yfin_data = pd.DataFrame(yf.download('MSFT', dt(2010,1,1), dt(2020,1,1)))
    stock_data = bt.feeds.PandasData(dataname=yfin_data)
    
    # Add data to Cerebro
    cerebro.adddata(stock_data)
    cerebro.addstrategy(MovingAverageStrategy)
    cerebro.addobserver(bt.observers.Value)
    cerebro.addanalyzer(bt.analyzers.SharpeRatio, riskfreerate=0)
    cerebro.addanalyzer(bt.analyzers.Returns)
    cerebro.addanalyzer(bt.analyzers.DrawDown)

    # Commission fees
    cerebro.broker.setcommission(0.01)


    #Run the strategy
    cerebro.broker.set_cash(3000)
    print('initial capital $%.2f' % cerebro.broker.getvalue())
    results = cerebro.run()

    #evaluate results
    print('Sharpe ratio: %.2f%%' % results[0].analyzers.sharperatio.get_analysis()['sharperatio'])
    print('Return: %.2f%%' % results[0].analyzers.returns.get_analysis()['rnorm100'])
    print('Drawdown: %.2f%%' % results[0].analyzers.drawdown.get_analysis()['max']['drawdown'])
    print('Capital $%.2f' % cerebro.broker.getvalue())
