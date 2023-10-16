# Strategies
import backtrader as bt

import pandas as pd
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
    params = (("vwap_period", 20),  )

    def __init__(self):
        self.vwap = bt.indicators.WeightedMovingAverage(self.data.close, period=self.params.vwap_period)
        ma_fast = bt.ind.SMA(period = 10)
        ma_slow = bt.ind.SMA(period = 50)
        self.crossover = bt.ind.CrossOver(ma_fast, self.vwap)

    def next(self):
        if not self.position:
            if self.crossover > 0:
                self.buy()
        elif self.crossover < 0:
            self.close()

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
