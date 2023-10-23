# auxiliary.py
from datetime import datetime
import backtrader as bt
import yfinance as yf
import backtrader.analyzers as btanalyzers
from strategies import *
import pandas as pd
import os
#

def reset_strategy(strategy, amount):
    strategy.broker.set_fundstartval(amount)  # Reset starting fund value for calculations
    strategy.broker.setcash(amount)  # Reset cash
    #strategy.broker.runstop()
    
    
def get_portfolio_stocks(portfolio):
    stocks = [data._name for data in portfolio.datas]
    return stocks
    pass

def get_portfolio_value_at_date(portfolio,strategy,date1,date2, amount):
    #print(strategy.broker.getvalue())
    # start to finish
    # 
    for ticker in portfolio:
        data = yf.download(ticker, start=date1, end=date2)
        data = bt.feeds.PandasData(dataname=data)
        cerebro = bt.Cerebro()  
        cerebro.adddata(data, name=ticker)
        cerebro.addanalyzer(btanalyzers.TradeAnalyzer, _name="trades")
        cerebro.addstrategy(strategy)
        cerebro.broker.setcash(amount)
        cerebro.addsizer(bt.sizers.PercentSizer, percents=10)
        back = cerebro.run()
    return(cerebro.broker.getvalue())

# this or that
def get_portfolio_tradelog(strategy):
    #print(strategy.trade_log)
    return(strategy.log)


def get_portfolio_information(strategy, specific_date):
    portfolio_value = get_portfolio_value_at_date(strategy,specific_date)
    stocks =get_portfolio_stocks(strategy)
    #num_trades = len(strategy.log)
    #open_positions = len(strategy)
    #total_pnl = sum(trade['PnL'] for trade in strategy.log)

    return {
        'Date': specific_date,
        'Portfolio Value': portfolio_value,
        'Stocks' : stocks,
        #'Number of Trades': num_trades,
        #'Open Positions': open_positions,
        #'Total Profit/Loss': total_pnl
    }
    pass

def get_portfolio_delta(portfolio,strategy, date1, date2,amount):
    # call get_portfolio_value on two seperate dates
    reset_strategy(strategy,amount)
    value = get_portfolio_value_at_date(portfolio, strategy, date1,date2,amount)
    
    delta = value - amount
    return delta
    pass

def get_weekly_portfolio_performance(strategy, date1, date2):
    # from date1 to date2, display performance %freq times where freq is 7
    frequency = 7  # Weekly
    performance_data = []
    current_date = date1

    while current_date <= date2:
        performance_data.append(get_portfolio_information(strategy, current_date))
        current_date += pd.DateOffset(days=frequency)
    print(performance_data)
    return performance_data

def get_daily_portfolio_performance(strategy, date1, date2):
    # from date1 to date2, display performance %freq times where freq is 1
    frequency = 1  # Daily
    performance_data = []
    current_date = date1
    while current_date <= date2:
        performance_data.append(get_portfolio_information(strategy, current_date))
        current_date += pd.DateOffset(days=frequency)

    print(performance_data)
    return performance_data
    pass

def get_hourly_portfolio_performance(strategy, date1, date2):
    # from date1 to date2, display performance %freq times where freq is one hour
    frequency = 1  # Hourly
    performance_data = []
    current_date = date1

    while current_date <= date2:
        performance_data.append(get_portfolio_information(strategy, current_date))
        current_date += pd.DateOffset(hours=frequency)
    print(performance_data)
    return performance_data
    pass

def get_piechart():
    # given portfolio distribution, display portfolio holdings with price and precentage
    pass

def dataframe_to_csv(dataframe, filename):
    # save dataframe to csv
    # make sure saved name doesnt exists. 
    # if yes, add a 0. 
    # if 0, add 1 to it. etc. 
    try:
        dataframe.to_csv(filename)
    except FileExistsError:
        # Handle filename conflicts by adding a number to the filename
        count = 0
        while True:
            count += 1
            new_filename = f"{filename}_{count}.csv"
            if not os.path.exists(new_filename):
                dataframe.to_csv(new_filename)
                break
    pass

def dataframe_to_JSON(dataframe, filename):
    # save dataframe to json
    # make sure saved name doesnt exists. 
    # if yes, add a 0. 
    # if 0, add 1 to it. etc. 
    try:
        dataframe.to_json(filename)
    except FileExistsError:
        # Handle filename conflicts by adding a number to the filename
        count = 0
        while True:
            count += 1
            new_filename = f"{filename}_{count}.json"
            if not os.path.exists(new_filename):
                dataframe.to_json(new_filename)
                break
    pass



