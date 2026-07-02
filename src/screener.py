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

years = pd.read_sql_query("""
    SELECT "Fiscal Years"
    FROM altman_z_score""", conn1)
years = list(years['Fiscal Years'])

def get_company_value(conn, metric, stock, year):
    query = f'SELECT {stock} FROM {metric} WHERE "Fiscal Years" = {year};'
    results  = pd.read_sql_query(query, conn).squeeze()
    return results

def get_industry_value(conn, metric, industry):
    query = f'SELECT {metric} from industries WHERE Industry = "{industry}"'
    results = pd.read_sql_query(query, conn).squeeze()
    return results

def compare_z_score(comp_conn, metric, stock, year):
    company_value = get_company_value(conn=comp_conn, metric=metric, stock=stock, year=year)
    if company_value >= 3:
        return 2
    elif company_value >= 2:
        return 1
    return 0

def compare_gpm(comp_conn, industry_conn, metric, stock, year, industry):
    company_value = get_company_value(conn=comp_conn, metric=metric, stock=stock, year=year)
    industry_value = get_industry_value(conn=industry_conn, metric=metric, industry=industry)
    if company_value >= industry_value:
        return 1
    return 0

def compare_pb_ratio(comp_conn, industry_conn, metric, stock, year, industry):
    company_value = get_company_value(conn=comp_conn, metric=metric, stock=stock, year=year)
    industry_value = get_industry_value(conn=industry_conn, metric=metric, industry=industry)
    if company_value < industry_value:
        return 1
    return 0

def compare_de_ratio(comp_conn, industry_conn, metric, stock, year, industry):
    company_value = get_company_value(conn=comp_conn, metric=metric, stock=stock, year=year)
    industry_value = get_industry_value(conn=industry_conn, metric=metric, industry=industry)
    if company_value < industry_value:
        return 1
    return 0

def compare_net_income_growth(comp_conn, metric, stock, year):
    company_value = get_company_value(conn=comp_conn, metric=metric, stock=stock, year=year)
    if company_value > 0:
        return 1
    return 0

def compare_revenue_growth(comp_conn, industry_conn, metric, stock, year, industry):
    company_value = get_company_value(conn=comp_conn, metric=metric, stock=stock, year=year)
    industry_value = get_industry_value(conn=industry_conn, metric=metric, industry=industry)
    if company_value >= industry_value:
        return 1
    return 0

for stock, industry in ind_dict.items():
    for year in years:


conn1.close()
conn2.close()