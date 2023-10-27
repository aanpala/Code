import psycopg2
import pandas as pd
from datetime import datetime
from methodsNEW import *
conn = establish_database_connection()
cur = conn.cursor()

#  call on seperate file ONCE.
#  push all versions on github. To keep track.

create_general_table_if_not_exists(cur)
create_income_statement_table_if_not_exists(cur)
create_balance_sheet_table_if_not_exists(cur)
create_cash_flow_table_if_not_exists(cur)

get_tickers_query = "SELECT symbol FROM sp500wiki;"
cur.execute(get_tickers_query)
tickers = [record[0] for record in cur.fetchall()]
tickers = tickers[0:10]

for ticker in tickers:
    a, b, c, d = pulldata([ticker])
    if not a.empty:
        rowa = a.iloc[0]  # gets each company data
        update_or_insert_general_data(cur, ticker, rowa)
    if not b.empty:
        rowb = b.iloc[0]  # gets each company data
        update_or_insert_income_statement_data(cur, ticker, rowb)  
    if not c.empty:
        rowc = c.iloc[0] 
        update_or_insert_balance_sheet_data(cur, ticker, rowc)
    if not d.empty:
        rowd = d.iloc[0]
        update_or_insert_cash_flow_data(cur, ticker, rowd)  

#dataframes = [a, b, c, d]  # Store your dataframes in a list

# update_insert_functions = [update_or_insert_general_data, update_or_insert_income_statement_data, update_or_insert_balance_sheet_data, update_or_insert_cash_flow_data]
# for ticker, dataframe, update_insert_function in zip(tickers, dataframes, update_insert_functions):
#     if not dataframe.empty:
#         row = dataframe.iloc[0]  
#         update_insert_function(cur, ticker, row) 

conn.commit()
cur.close()
conn.close()
