import yfinance as yf
from SP500Wiki import *
from methodsNEW import *


conn = establish_database_connection()
cur = conn.cursor()

# Ticker Extraction
get_tickers_query = "SELECT symbol FROM sp500wiki;"
cur.execute(get_tickers_query)
tickers = [record[0] for record in cur.fetchall()]
tickers = tickers[0:4]

# Financial dataframes
income_statement_Q = pd.DataFrame()
income_statement_Y = pd.DataFrame()
balance_sheet_Q = pd.DataFrame()
balance_sheet_Y = pd.DataFrame()
cashflow_Q = pd.DataFrame()
cashflow_Y = pd.DataFrame()


# IS quarterly
for ticker_symbol in tickers:
    ticker = yf.Ticker(ticker_symbol)
    df = ticker.quarterly_income_stmt.T
    df['Ticker'] = ticker_symbol
    #print(df['Ticker'])
    df['Date'] = df.index.strftime('%Y-%m-%d')
    #print(df['Date'])

    if not df.empty:
        cur = conn.cursor()
        for _, row in df.iterrows():  # Iterate through all rows of data
            print(ticker)
            update_or_insert_yf_income_statement_data(cur, ticker_symbol, row)
        conn.commit()  # Commit changes to the database
        cur.close()
    #print(df)

    # Concatenate the data to your income_statement_Q DataFrame
    income_statement_Q = pd.concat([income_statement_Q, df])

# Display the combined data for all stocks
#print(income_statement_Q)
   
#IS annual

# BS quarterly
for ticker_symbol in tickers:
    ticker = yf.Ticker(ticker_symbol)
    df = ticker.quarterly_balance_sheet.T
    df['Ticker'] = ticker_symbol
    df['Date'] = df.index.strftime('%Y-%m-%d')
    if not df.empty:
        cur = conn.cursor()
        for _, row in df.iterrows():  # Iterate through all rows of data
            update_or_insert_yf_balance_sheet_data(cur, ticker_symbol, row)
        conn.commit()  # Commit changes to the database
        cur.close()
    #print(df)
    # Concatenate the data to your income_statement_Q DataFrame
    balance_sheet_Q = pd.concat([balance_sheet_Q, df])



# CF quarterly
# Repurchase Of Capital Stock
for ticker_symbol in tickers:
    ticker = yf.Ticker(ticker_symbol)
    df = ticker.quarterly_cashflow.T
    df['Ticker'] = ticker_symbol
    df['Date'] = df.index.strftime('%Y-%m-%d')
    if not df.empty:
        cur = conn.cursor()
        for _, row in df.iterrows():  # Iterate through all rows of data
            update_or_insert_yf_cash_flow_data(cur, ticker_symbol, row)
        conn.commit()  # Commit changes to the database
        cur.close()
    #print(df)
    # Concatenate the data to your income_statement_Q DataFrame
    cashflow_Q = pd.concat([cashflow_Q, df])
#print(cashflow_Q)

# # CF annual