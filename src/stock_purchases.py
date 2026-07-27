from datetime import datetime
from financial_metrics.financial_statements import get_income_statement
import math
import pandas as pd
import sqlite3 as sql
import yfinance as yf
import os
from dotenv import load_dotenv

load_dotenv()
fmp_key = os.getenv('FMP_API_KEY')

MONEY = 30000
purchase_dict = {}
current_holdings = []
df_purchased = pd.DataFrame({
    "fiscal_years": pd.Series(dtype='int'),
    "filing_date": pd.Series(dtype='datetime64[ns]'),
    "stocks": pd.Series(dtype='str'),
    "purchase_price": pd.Series(dtype='float64'),
    "shares": pd.Series(dtype='int'),
    "total_value": pd.Series(dtype='float64'),
    "purchase_type": pd.Series(dtype='str'),
})

conn = sql.connect("../data/screener_results.db")
cursor = conn.cursor()

# Return list of stocks and years for the for loop
stock_year_query = pd.read_sql_query("""SELECT stocks, fiscal_years
                                     FROM screener_results ORDER BY stocks""", conn)
stocks_list = stock_year_query['stocks'].to_list()
stocks = list(dict.fromkeys(stocks_list))
years_list = stock_year_query['fiscal_years'].to_list()
years = list(dict.fromkeys(years_list))
first_year = years[0]
remaining_years = years[1:]

# Query screener results
df_screened = pd.read_sql_query("""SELECT *
                                        FROM screener_results;""", conn)

def get_ranking(stock, year, screener_results):
    # Returns the point values from the screener results database
    target_row = screener_results.loc[(screener_results['fiscal_years'] == year) &
                                 (screener_results['stocks'] == stock)]
    points = target_row['result'].iloc[0]
    return points

def get_filing_date(stock, year, screener_results):
    # Returns the filing date
    target_row = screener_results.loc[(screener_results['fiscal_years'] == year) &
                                      (screener_results['stocks'] == stock)]
    filing_date = target_row['filing_date'].iloc[0]
    return filing_date

def get_purchase_price(stock, target_date):
    yf_ticker = yf.Ticker(stock)
    price_history = yf_ticker.history(period='1y', start=target_date)
    start_price = price_history.iloc[0]['Close']
    return start_price

def purchase_shares(stock, target_date, cash):
    purchase_price = get_purchase_price(stock=stock, target_date=target_date)
    no_of_shares = cash / purchase_price
    shares_int = math.floor(no_of_shares)
    value_inv = shares_int * purchase_price
    return purchase_price, shares_int, value_inv

# split the for loop into 2 parts
# Part 1 is just for the first year
# Part 2 is for any subsequent year

# Year 1
for s in stocks:
    p = get_ranking(stock=s, year=first_year, screener_results=df_screened)
    if p > 5:
        current_holdings.append(s)

# Calculate amount of cash to invest in each company in the initial year
cash_per_co = MONEY / len(current_holdings)

#Purchase stocks for the first year
for s in current_holdings:
    fd = get_filing_date(stock=s, year=first_year, screener_results=df_screened)
    price, shares, value = purchase_shares(stock=s, target_date=fd, cash=cash_per_co)
    new_row_data = [first_year, fd, s, price, shares, value, 'Buy']
    new_row_dict = dict(zip(df_purchased.columns, new_row_data))
    df_new_row = pd.DataFrame([new_row_dict])
    df_purchased = pd.concat([df_purchased, df_new_row], ignore_index=True)

# for y in years:
#     for s in stocks:
#         p = get_ranking(stock=s, year=y, screener_results=df_screened)
#         if p > 5:
#             current_holdings.append(s)




#
#
# for y in years:
#     purchase_list = []
#     for s in stocks:
#         p = get_ranking(stock=s, year=y)
#         if p >=5:
#             purchase_list.append(s)
#     # Add results to purchase dictionary that includes years as key and list of stocks as values
#     purchase_dict[y] = purchase_list
#
# for y, sl in purchase_dict.items():
#     y_string = str(y)
#     for stock in sl:
#         loop = 0
#         if stock not in current_holdings:
#              current_holdings.append(stock)
#         income_statement = get_income_statement(t=stock, key=fmp_key)
#         income_statement.reverse() # Reverse income statement for ascending order
#         for i in income_statement: # For matching fiscal year with filing date
#             if i['fiscalYear'] == y_string:
#                 filing_date = i['filingDate']
#                 stock_price = get_purchase_price(stock=stock, target_date=filing_date)
#                 purchase_date = datetime.strptime(filing_date, '%Y-%m-%d').date()
#                 shares = math.floor(MONEY / stock_price)
#                 new_row = pd.DataFrame([{"Fiscal Years": y,
#                                         "Filing Date": filing_date,
#                                         "Company": stock,
#                                          "Purchase Price": stock_price,
#                                          "Shares": shares,
#                                          "Type": "Purchase",}])
#                 df_purchased = pd.concat([df_purchased, new_row])
#
#
#         loop += 1
#         if loop >= 1:
#             if stock in current_holdings:



conn.close()
