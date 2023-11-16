# Code

The set of calls 

1. Ensure method and strategies files is in same folder as respective code.
2. run CreateTable.py
3. run SP500wiki.py to extract all stock tickers in S&P500 according to Wikipedia.
4. run pulldata2.py to update SQL tables: General information, Income Statement, Balance Sheet and Cashflow data.
5. run pullPrice.py to get daily price and intraday price data for all stocks within a set timeperiod from Yahoo Finance.
6. Execute backtraderonSQL to establish connection between SQL files and python code. This is where we will test out traidng algorithms
7. Perfromance and holdings data will be saved in files here


1. Create a system that pulls price and fundamental data and can run daily without intervention.
2. 2. Set up a backtrader strategy using the collected data. 3. Clean up the code and make it efficient. 4. Set up ec2, install postgres and deploy the data collector code in the ec2. We are now collecting data daily. Also, connect to cloud database from local machine. 5. Save and load strategies and their results to/from the database -- now we can only work on strategies -- 6. Create custom indicators on backtrader library 7. See portfolio performance through quantstats library 8. Load intraday price(minute) through data collection system 9. Run strategies on intraday 10. Add more instruments and their data in the database - MF, Indexes, Bonds 11. Run strategies on different instruments.
