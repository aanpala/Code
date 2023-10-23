#libraries
import backtrader as bt
import pandas as pd


class Basic(bt.Strategy):
    def __init__(self):
        self.sma = bt.indicators.SimpleMovingAverage(self.data, period=20)
    def next(self):
        if self.data.close[0] > self.sma[0]:
            self.buy()
        else:
            self.sell()

class MyStrategy1(bt.Strategy):
    params =  (
        ('rsi_period', 14),
        ('rsi_overbought', 70),
        ('rsi_oversold', 30),
        ('vwap_period', 20))
    
    def __init__(self):
        self.portfolio_value = []  # List to store portfolio values


    def next(self):
        rsi_value = self.rsi[0]
        portfolio_value = self.broker.get_value()
        
        # Access stocks and their quantities in the portfolio
        for data in self.datas:
            stock_name = data._name  # Name of the stock
            stock_quantity = self.getposition(data).size
            print(f"{stock_name}: {stock_quantity}")
        print(f"Portfolio Value: {portfolio_value}")
        self.portfolio_value.append(portfolio_value)
        
        if rsi_value < 30 and not self.crossed_30:
                self.crossed_30 = True
                self.crossed_70 = False
                self.log("RSI crossed below 30 - Buy Signal")

        if rsi_value > 70 and not self.crossed_70:
            self.crossed_30 = False
            self.crossed_70 = True
            self.log("RSI crossed above 70 - Sell Signal")

        vwap_value = self.vwap[0]

        if self.data.close[0] > vwap_value and rsi_value < 30:
            print("BUY")
            self.buy()

        if self.data.close[0] < vwap_value and rsi_value > 70:
            print("SELL")

            self.sell()
            

        
class TestStrategy(bt.Strategy):
# trade after 5 days no matter
    def log(self, txt, dt=None):
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))

    def __init__(self):
        self.dataclose = self.datas[0].close
        self.order = None
        self.bar_executed = 0
        self.stop_loss = 0  # Initialize stop loss level
        self.take_profit = 0  # Initialize take profit level

    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            return
        if order.status in [order.Completed]:
            if order.isbuy():
                self.log("BUY EXECUTED at {}".format(order.executed.price))
            elif order.issell():
                self.log("SELL EXECUTED at {}".format(order.executed.price))
            self.bar_executed = len(self)
        self.order = None

    def next(self):
        self.log('Close, %.2f' % self.dataclose[0])

        if self.order:
            return

        if not self.position:
            if self.dataclose[0] < self.dataclose[-1]:
                if self.dataclose[-1] < self.dataclose[-2]:
                    self.log('BUY CREATE, %.2f' % self.dataclose[0])
                    self.order = self.buy()
                    self.stop_loss = self.dataclose[0] - (2 * (self.dataclose[0] - self.dataclose[-1]))  # Set stop loss
                    self.take_profit = self.dataclose[0] + (2 * (self.dataclose[0] - self.dataclose[-1]))  # Set take profit
        else:
            if len(self) >= (self.bar_executed + 5) or self.dataclose[0] <= self.stop_loss:
                if self.dataclose[0] <= self.stop_loss:
                    self.log("STOPPED OUT")
                elif self.dataclose[0] >= self.take_profit:
                    self.log("TAKE PROFIT")
                else:
                    self.log('SELL CREATED at {}'.format(self.dataclose[0]))
                self.order = self.sell()


        # Add a condition for a sell signal
        #elif self.dataclose[0] > self.dataclose[-1]:
         #   if self.dataclose[-1] > self.dataclose[-2]:

               # SELL, SELL, SELL!!! (with all possible default parameters)
#                self.log('SELL CREATE, %.2f' % self.dataclose[0])
#                self.sell()

class MaCrossStrategy(bt.Strategy):
 
    def __init__(self):
        ma_fast = bt.ind.SMA(period = 10)
        ma_slow = bt.ind.SMA(period = 50)
         
        self.crossover = bt.ind.CrossOver(ma_fast, ma_slow)
 
    def next(self):
        if not self.position:
            if self.crossover > 0: 
                self.buy()
        elif self.crossover < 0: 
            self.close()
            
class SmartCross(bt.Strategy):
    params = (
        ('rsi_period', 14),
        ('rsi_overbought', 70),
        ('rsi_oversold', 30),
        ('vwap_period', 20))

    def __init__(self):
        self.vwap = {}
        self.crossover = {}
        self.stop_loss = {}
        self.take_profit = {}
        self.rsi = {}
        self.trade_history = {}
        self.previous_portfolio_value = self.broker.getvalue()
        self.previous_position_count = {}

        for data in self.datas:
            self.vwap[data] = bt.indicators.WeightedMovingAverage(data.close, period=self.params.vwap_period)
            ma_fast = bt.ind.SMA(period=10)
            ma_slow = bt.ind.SMA(period=50)
            self.crossover[data] = bt.ind.CrossOver(ma_fast, self.vwap[data])
            self.stop_loss[data] = 0
            self.take_profit[data] = 0
            self.rsi[data] = bt.indicators.RelativeStrengthIndex(data.close, period=self.params.rsi_period)
            self.trade_history[data] = []
            self.previous_position_count[data] = 0

    def log_trade(self, trade, data):
        dt_open = trade.data.datetime.datetime()
        dt_close = self.datetime.datetime()
        price_open = trade.price
        price_close = trade.price
        psize = trade.size
        pnl = trade.pnl
        self.trade_history[data].append({
            'Date Open': dt_open,
            'Date Close': dt_close,
            'Price Open': price_open,
            'Price Close': price_close,
            'Size': psize,
            'PnL': pnl
        })

        # Print the trade information
        trade_df = pd.DataFrame(self.trade_history[data])
        self.log(f"Trade Information for {data._name}:")
        self.log(trade_df)

    def print_portfolio(self):
        for data in self.datas:
            portfolio_data = []
            position = self.getposition(data)
            
            # Calculate price change from previous day
            current_price = data.close[0]
            previous_close = data.close[-1]  # Assuming your data has the previous day's closing price
            price_change = current_price - previous_close
            
            profit_loss = price_change * position.size
            portfolio_data.append({
                'Ticker': data._name,
                'Quantity': position.size,
                'Price Change': price_change,
                'Profit/Loss': profit_loss
            })

        print(f"Portfolio Contents for {data._name}:")
        for entry in portfolio_data:
            pass
            print(f"Ticker: {entry['Ticker']}, Quantity: {entry['Quantity']}, Price Change: {entry['Price Change']}, Profit/Loss: {entry['Profit/Loss']},")

    def next(self):
        for data in self.datas:
            close_price = data.close[0]
            open_price = data.open[0]

            if not self.position and self.crossover[data] > 0:
                #print(f"BUY SIGNAL for {data._name}")
                self.buy(data=data)
                self.stop_loss[data] = data.close[0] - 2 * (data.close[0] - data.close[-1])
                self.take_profit[data] = data.close[0] + 2 * (data.close[0] - data.close[-1])
            elif self.position and (self.crossover[data] < 0 or close_price <= self.stop_loss[data] or close_price >= self.take_profit[data]):
                if close_price <= self.stop_loss[data]:
                    print(f"STOPPED OUT for {data._name}")
                elif close_price >= self.take_profit[data]:
                    print(f"TAKE PROFIT for {data._name}")
                else:
                    print(f"SELL SIGNAL for {data._name}")
                self.close(data=data)

        self.print_portfolio()
        current_portfolio_value = self.broker.getvalue()
        portfolio_change = current_portfolio_value - self.previous_portfolio_value
        print(f"Portfolio Value: {current_portfolio_value:.2f}, Change: {portfolio_change:.2f}")
        self.previous_portfolio_value = current_portfolio_value


class RSI_VWAP_Strategy(bt.Strategy):
    params = (
        ("vwap_period", 20),
        ("rsi_period", 14),  # RSI period
        ("rsi_overbought", 70),  # RSI overbought level
        ("rsi_oversold", 30)  # RSI oversold level
    )

    def __init__(self):
        self.vwap = bt.indicators.WeightedMovingAverage(self.data.close, period=self.params.vwap_period)
        self.crossover = bt.ind.CrossOver(self.data.close, self.vwap)
        self.rsi = bt.indicators.RelativeStrengthIndex(period=self.params.rsi_period)
        self.order = None

    def next(self):
        if self.order:
            return

        if not self.position:
            if self.crossover > 0:
                if self.rsi < self.params.rsi_oversold:
                    self.buy()
        else:
            if self.crossover < 0 or self.rsi > self.params.rsi_overbought:
                self.close()
                
class ReversalStrategy(bt.Strategy):
    params = (
        ("vwap_period", 20),    # VWAP calculation period
        ("rsi_period", 14),     # RSI period
        ("rsi_overbought", 70), # RSI overbought level
        ("rsi_oversold", 30),   # RSI oversold level
        ("macd_short_period", 12),  # MACD short-term period
        ("macd_long_period", 26),   # MACD long-term period
        ("macd_signal_period", 9),  # MACD signal period
    )

    def __init__(self):
        self.vwap = bt.indicators.WeightedMovingAverage(self.data.close, period=self.params.vwap_period)
        self.rsi = bt.ind.RelativeStrengthIndex(period=self.params.rsi_period)
        self.macd = bt.ind.MACD(
            period_me1=self.params.macd_short_period,
            period_me2=self.params.macd_long_period,
            period_signal=self.params.macd_signal_period
        )

    def next(self):
        if self.order:
            return

        if not self.position:
            if self.rsi < self.params.rsi_oversold and self.data.close[0] > self.vwap[0] and self.macd.macd[0] > self.macd.signal[0]:
                self.buy()
        else:
            if self.rsi > self.params.rsi_overbought or self.macd.macd[0] < self.macd.signal[0]:
                self.close()
                
class VWAP(bt.Indicator):
    alias = ('VWAP',)

    params = (
        ('period', 20),  # VWAP calculation period
    )

    lines = ('vwap',)

    def __init__(self):
        self.lines.vwap = bt.indicators.WeightedMovingAverage(self.data.close, period=self.params.period)
        self.cum_volume = bt.indicators.SumN(self.data.volume, period=self.params.period)

    def next(self):
        self.lines.vwap[0] = self.lines.vwap[-1] + (self.data.close[0] * self.data.volume[0])
        self.lines.vwap[0] /= self.cum_volume[0]

class VWAPRSIStrategy(bt.Strategy):
    params = (
        ("vwap_period", 20),
        ("rsi_period", 14),
        ("rsi_overbought", 70),
        ("rsi_oversold", 30)
    )

    def __init__(self):
        self.dataclose = self.datas[0].close
        self.datavwap = VWAP(self.datas[0], period=self.params.vwap_period)
        self.rsi = bt.indicators.RelativeStrengthIndex(period=self.params.rsi_period)
        self.order = None

    def next(self):
        if self.order:
            return

        if self.rsi < self.params.rsi_oversold and self.dataclose[0] > self.datavwap[0]:
            self.order = self.buy()
        elif self.rsi > self.params.rsi_overbought and self.dataclose[0] < self.datavwap[0]:
            self.order = self.sell()

    def notify_order(self, order):
        if order.status in [order.Completed, order.Canceled, order.Margin, order.Rejected]:
            self.order = None
