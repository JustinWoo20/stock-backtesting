from datetime import datetime
from financial_metrics.financial_statements import get_income_statement
import math
import pandas as pd
import sqlite3 as sql
import yfinance as yf
import os
from dotenv import load_dotenv

load_dotenv()
# TODO: Divide money based on length of list
fmp_key = os.getenv('FMP_API_KEY')

MONEY = 10000
purchase_dict = {}
current_holdings = []
df_purchased = pd.DataFrame({
    "Fiscal Years": pd.Series(dtype='int'),
    "Filing Date": pd.Series(dtype='datetime64[ns]'),
    "Company": pd.Series(dtype='str'),
    "Purchase Price": pd.Series(dtype='float64'),
    "Shares": pd.Series(dtype='int'),
    "Type": pd.Series(dtype='str'),
})

conn = sql.connect("../data/screener_results.db")
cursor = conn.cursor()
cursor.execute("SELECT * FROM screener_results LIMIT 0")
c = [description[0] for description in cursor.description] # Get stocks from screener results
stocks = c[1:]

years_query= pd.read_sql_query('SELECT "Fiscal Years" FROM screener_results', conn).values
years = years_query.squeeze()
years = years.tolist()

def get_ranking(stock, year):
    # Returns the point values from the screener results database
    point_value_query = f'SELECT {stock} FROM screener_results WHERE "Fiscal Years" == {year}'
    points = pd.read_sql_query(point_value_query, conn).squeeze()

    return int(points)

def get_stock_price(stock, target_date):
    yf_ticker = yf.Ticker(stock)
    price_history = yf_ticker.history(period='1d', start=target_date)
    closing_price = price_history['Close']
    return closing_price

def purchase_share(stock, target_date, cash):
    price = get_stock_price(stock=stock, target_date=target_date)
    shares = cash / price
    return price, shares


for y in years:
    purchase_list = []
    for s in stocks:
        p = get_ranking(stock=s, year=y)
        if p >=5:
            purchase_list.append(s)
    # Add results to purchase dictionary that includes years as key and list of stocks as values
    purchase_dict[y] = purchase_list

for y, sl in purchase_dict.items():
    y_string = str(y)
    for stock in sl:
        if stock not in current_holdings:
             current_holdings.append(stock)
        income_statement = get_income_statement(t=stock, key=fmp_key)
        income_statement.reverse()
        for i in income_statement: # For matching fiscal year with filing date
            if i['fiscalYear'] == y_string:
                filing_date = i['filingDate']
                purchase_date = datetime.strptime(filing_date, '%Y-%m-%d').date()
                stock_price = get_stock_price(stock=stock, target_date=i['filingDate'])
                stock_price = stock_price.iloc[0]
                shares = math.floor(MONEY / stock_price)
                new_row = pd.DataFrame([{"Fiscal Years": y,
                                        "Filing Date": filing_date,
                                        "Company": stock,
                                         "Purchase Price": stock_price,
                                         "Shares": shares,
                                         "Type": "Purchase",}])
                df_purchased = pd.concat([df_purchased, new_row])

conn.close()
