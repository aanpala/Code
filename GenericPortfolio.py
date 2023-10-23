import datetime
import backtrader as bt
import backtrader.analyzers as btanalyzers
import yfinance as yf
import matplotlib.pyplot as plt
from strategies import *
import pandas as pd
import seaborn

weightings = {"AAPL":"25", "AMZN":"25", "KO":"25","QSR":"25"}
stocks = ["AAPL", "AMZN", "KO","QSR"]

def POrtoflioCALc(weightings, data, name):
    data[name] = sum([int(weightings[x])*data[x]/100 for x in list(weightings.keys())])
    return data

basedata = yf.Ticker(stocks[0]).history(period="5y").reset_index()[["Date","Open"]]
basedata["Date"] = pd.to_datetime(basedata["Date"])
basedata= basedata.rename(columns ={"Open":stocks[0]})

# print(basedata)
if (len(stocks)>1):
    for x in range(1, len(stocks)):
        newdata = yf.Ticker(stocks[x]).history(period="5y").reset_index()[["Date","Open"]]
        newdata["Date"] = pd.to_datetime(basedata["Date"])
        newdata = newdata.rename(columns ={"Open":stocks[x]})
        basedata = pd.merge(basedata, newdata, on="Date")
#print(basedata)

# 
basedata= basedata[basedata["Date"] > "2021-03-03"]


# normalize
for x in stocks:
    basedata[x] = basedata[x]/(basedata[x].iloc[0])
    
basedata = POrtoflioCALc(weightings, basedata, "Our Portfolio")
plt.plot(basedata["Date"], basedata["Our Portfolio"], label = "Our Portfolio")
#plt.style.use("seaborn")
plt.legend(loc="upper left")
plt.show()
print(basedata)


