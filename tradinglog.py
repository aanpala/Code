import datetime
import backtrader as bt
import backtrader.analyzers as btanalyzers
import yfinance as yf
from strategies import *

tickers = {"AAPL": 1.0}

for ticker, target in tickers.items():
    data = yf.download(ticker, start="2010-01-01", end="2020-12-31")
    data = bt.feeds.PandasData(dataname=data)
    data.target = target

    cerebro = bt.Cerebro()  
    cerebro.adddata(data, name=ticker)
    cerebro.addstrategy(SmartCross)
    cerebro.broker.setcash(1000000.0)
    cerebro.addsizer(bt.sizers.PercentSizer, percents=10)

    cerebro.addanalyzer(btanalyzers.SharpeRatio, _name="sharpe")
    cerebro.addanalyzer(btanalyzers.Transactions, _name="trans")
    cerebro.addanalyzer(btanalyzers.TradeAnalyzer, _name="trades")

    print(f'Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())
    back = cerebro.run()
    print(f'Final Portfolio Value: %.2f' % cerebro.broker.getvalue())

    sharpe = back[0].analyzers.sharpe.get_analysis()
    trans = back[0].analyzers.trans.get_analysis()
    trades = back[0].analyzers.trades.get_analysis()

    cerebro.plot()[0]

# Define a list of specific dates for analysis
specific_dates = ["2013-01-05", "2016-07-04", "2019-01-01"]

for date in specific_dates:
    specific_date = datetime.datetime.strptime(date, "%Y-%m-%d").date()

    try:
        data = yf.download(ticker, start="2010-01-01", end=specific_date)
        data = bt.feeds.PandasData(dataname=data)
        data.target = target

        cerebro = bt.Cerebro()
        cerebro.adddata(data, name=ticker)
        cerebro.addstrategy(SmartCross)
        cerebro.broker.setcash(1000000.0)
        cerebro.addsizer(bt.sizers.PercentSizer, percents=10)

        back = cerebro.run()
        print(f'Portfolio Value on {specific_date}: %.2f' % cerebro.broker.getvalue())
        print(((cerebro.broker.getvalue() / 1000000.0) - 1) * 100)

    except Exception as e:
        print(f"Data is not available for {specific_date}. Error: {e}")
