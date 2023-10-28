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
# DONE
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
            update_or_insert_yf_income_statement_data(cur, ticker_symbol, row)
        conn.commit()  # Commit changes to the database
        cur.close()
    #print(df)

    # Concatenate the data to your income_statement_Q DataFrame
    income_statement_Q = pd.concat([income_statement_Q, df])

# Display the combined data for all stocks
print(income_statement_Q)
   
# IS annual
# for ticker_symbol in tickers:
#     ticker = yf.Ticker(ticker_symbol)
#     df = ticker.income_stmt.T
#     df['Ticker'] = ticker_symbol
#     df['Date'] = df.index.strftime('%Y-%m-%d')
#     if not df.empty:
#         cur = conn.cursor()
#         for _, row in df.iterrows():  # Iterate through all rows of data
#             pass
#             #update_or_insert_yf_income_statement_data(cur, ticker_symbol, row)
#         conn.commit()  # Commit changes to the database
#         cur.close()
#     #print(df)

#    income_statement_Y = pd.concat([income_statement_Y, df])

#print(income_statement_Y)

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

# Display the combined data for all stocks
#print(balance_sheet_Q)

# # BS annual
# for ticker_symbol in tickers:
#     ticker = yf.Ticker(ticker_symbol)
#     df = ticker.balance_sheet.T
#     df['Ticker'] = ticker_symbol
#     df['Date_Ticker'] = df['Ticker'] + "." +  df.index.strftime('%Y-%m-%d')     #
#     df = df.reset_index(drop=True)
#     balance_sheet_Y = pd.concat([balance_sheet_Y, df])
#     balance_sheet_Y = balance_sheet_Y.reset_index(drop=True)

# #print(balance_sheet_Y)


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
# for ticker_symbol in tickers:
#     ticker = yf.Ticker(ticker_symbol)
#     df = ticker.cashflow.T
#     df['Ticker'] = ticker_symbol
#     df['Date_Ticker'] = df['Ticker'] + "." +  df.index.strftime('%Y-%m-%d') 
#     #df = df.reset_index(drop=True)
#     cashflow_Y = pd.concat([cashflow_Y, df])
#     cashflow_Y = cashflow_Y.reset_index(drop=True)

# #print(cashflow_Y)






# # show meta information about the history (requires history() to be called first)
# #print(msft.history_metadata)


# #print(msft.actions)
# #print(msft.dividends)
# #print(msft.splits)
# #print(msft.capital_gains)  # only for mutual funds & etfs

# # show share count
# #print(msft.get_shares_full(start="2022-01-01", end=None))

# # show financials:
# # - income statement
# #print(msft.income_stmt)
# #print(msft.quarterly_income_stmt)
# # - balance sheet
# #print(msft.balance_sheet)
# #print(msft.quarterly_balance_sheet)
# # - cash flow statement
# #print(msft.cashflow)
# #print(msft.quarterly_cashflow)

# #print(msft.earnings_dates)