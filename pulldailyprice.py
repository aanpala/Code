import yfinance as yf
import pandas as pd
from SP500Wiki import *
from methodsNEW import *


conn = establish_database_connection()
cur = conn.cursor()

# Ticker Extraction
get_tickers_query = "SELECT symbol FROM sp500wiki;"
cur.execute(get_tickers_query)
tickers = [record[0] for record in cur.fetchall()]
tickers = tickers[0:4]

# Create the daily price data table
create_daily_price_data(cur)

# Daily dataframes
startdate = "2023-01-24"
enddate = "2023-02-20"

for ticker_symbol in tickers:
    ticker = yf.Ticker(ticker_symbol)
    data = ticker.history(start=startdate, end=enddate)
    if not data.empty:
        data['Ticker'] = ticker_symbol
        data.reset_index(inplace=True)
        data['Date'] = data['Date'].dt.strftime('%Y-%m-%d')
        data_list = data.to_dict('records')  # Convert DataFrame to a list of dictionaries

        # Bulk insert data into the database
        for row in data_list:
            update_or_insert_yf_daily_data(cur, ticker_symbol, row)

# Commit changes to the database and close the cursor
conn.commit()
cur.close()
