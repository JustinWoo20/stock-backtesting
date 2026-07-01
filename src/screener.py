import sqlite3 as sql
from financial_metrics.altman_z_score import get_industry
import pandas as pd

conn1 = sql.connect("../data/financial_metrics.db")
conn2 = sql.connect("../data/industry_averages.db")

cursor1 = conn1.cursor()
cursor2 = conn2.cursor()

financial_metrics = ['altman_z_score', 'gpm', 'pb_ratio', 'de_ratio', 'net_income_growth', 'revenue_growth']
test_stocks = ['AAPL', 'TSLA', 'AMZN']
software_ind = ['Software - Application', 'Internet Content & Information',]

ind_dict = {}
for stock in test_stocks:
    ind = get_industry(ticker=stock)
    ind_dict[stock] = ind

print(ind_dict)

years = pd.read_sql_query("""
    SELECT "Fiscal Years"
    FROM altman_z_score""", conn1)
years = list(years['Fiscal Years'])

def get_company_value(conn, table, stock, year):
    query = f'SELECT {stock} FROM {table} WHERE "Fiscal Years" = {year};'
    results  = pd.read_sql_query(query, conn).squeeze()
    return results

def get_industry_value(conn, metric, industry):
    query = f'SELECT {metric} from industries WHERE Industry = "{industry}"'
    results = pd.read_sql_query(query, conn).squeeze()
    return results

def compare_z_score(company_value):
    points = 0
    z_score = company_value
    if z_score >= 3:
        points += 2
    elif z_score >= 2:
        points += 1
    else:
        points += 0

    return points

def compare_gpm(company_value, industry_value):
    points = 0
    company_gpm = company_value
    industry_gpm = industry_value
    if company_gpm > industry_gpm:
        points += 1
    else:
        points += 0
    return points


conn1.close()
conn2.close()