from datetime import datetime
from financial_metrics.financial_statements import get_income_statement
import pandas as pd
import sqlite3 as sql
import yfinance as yf
import os
from dotenv import load_dotenv
load_dotenv()

fmp_key = os.getenv('FMP_API_KEY')

starting_money = 30000

conn = sql.connect("../data/screener_results.db")
cursor = conn.cursor()
cursor.execute("SELECT * FROM screener_results LIMIT 0")
c = [description[0] for description in cursor.description] # Get stocks from screener results
stocks = c[1:]

years_query= pd.read_sql_query('SELECT "Fiscal Years" FROM screener_results', conn).values
years = years_query.squeeze()

def get_ranking(stock, year):
    # Returns the point values from the screener results database
    point_value_query = f'SELECT {stock} FROM screener_results WHERE "Fiscal Years" == {year}'
    points = pd.read_sql_query(point_value_query, conn).squeeze()

    return int(points)

def get_stock_price(stock, target_date):
    yfticker = yf.Ticker(stock)
    price_history = yfticker.history(period='1d', start=target_date)
    closing_price = price_history['Close']
    return closing_price

# def purchase_shares(price, money):


for y in years:
    for s in stocks:
        p = get_ranking(stock=s, year=y)
        if p >=5:
            income_statement = get_income_statement(t=s, key=fmp_key)
            income_statement.reverse()
            for i in income_statement: # Automatically matches fiscal year with its respective filing date
                if i['fiscalYear'] == y:
                    filing_date = i['filingDate']
                    stock_price = get_stock_price(stock=s, target_date=filing_date)




        # else:
        #     d = make_decision(number=p)

conn.close()
# def buy_decision(stock_dict):
#     for stock, years in stock_dict.items():
#         for year in years:
#             balance_sheet = get_balance_sheet(t=stock, key=fmp_key)
#
#
#
# for stock, years in test_dict.items():
#     for y, points in years.items():
#         if points >= 5:
#             balance_sheet = get_balance_sheet(t=stock, key=fmp_key)
#
#
#
#

# def get_yf_ticker(ticker):
#     ticker_obj = yf.Ticker(ticker)
#     h = ticker_obj.history(period='6y')
#     print(h[h['Dividends'] != 0.0])
#     print(h[h['Stock Splits'] != 0.0])
#     dividends = ticker_obj.get_dividends()
#     print(dividends)
# get_yf_ticker('AAPL')