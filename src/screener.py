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

# Match companies with their respective industry
ind_dict = {}
for stock in test_stocks:
    ind = get_industry(ticker=stock)
    ind_dict[stock] = ind

years = pd.read_sql_query("""
    SELECT "Fiscal Years"
    FROM altman_z_score""", conn1)
years = list(years['Fiscal Years'])
years.reverse()
years = [int(y) for y in years]

def get_company_value(conn, metric, stock, year):
    # Query financial metrics database to find a company's respective value
    query = f'SELECT {stock} FROM {metric} WHERE "Fiscal Years" = {year};'
    results  = pd.read_sql_query(query, conn).squeeze()
    return results

def get_industry_value(conn, metric, industry):
    # Query the industry averages db to find the average value for a company's industry
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

# {'AAPL: {2021: 5, 2022: 3...}, 'TSLA: {2021; 3, 2022: 5...}}
results_dict = {}

for stock, industry in ind_dict.items():
    inside_list = []
    for year in years:
        total_points = 0
        z_score_points = compare_z_score(comp_conn=conn1, metric='altman_z_score', stock=stock, year=year)
        total_points += z_score_points
        gpm_points = compare_gpm(comp_conn=conn1, industry_conn=conn2, metric='gpm', stock=stock, year=year, industry=industry)
        total_points += gpm_points
        pb_points = compare_pb_ratio(comp_conn=conn1, industry_conn=conn2, metric='pb_ratio', stock=stock, year=year, industry=industry)
        total_points += pb_points
        de_points = compare_de_ratio(comp_conn=conn1, industry_conn=conn2, metric='de_ratio', stock=stock, year=year, industry=industry)
        total_points += de_points
        ni_growth_points = compare_net_income_growth(comp_conn=conn1, metric='net_income_growth', stock=stock, year=year)
        total_points += ni_growth_points
        rev_growth_points = compare_revenue_growth(comp_conn=conn1, industry_conn=conn2, metric='revenue_growth', stock=stock, year=year, industry=industry)
        total_points += rev_growth_points
        inside_list.append(total_points)

    results_dict[stock] = inside_list

screener_results = pd.DataFrame.from_dict(data=results_dict)
screener_results.insert(value=years, loc=0, column='Fiscal Years')
conn3 = sql.connect("../data/screener_results.db")
cursor3 = conn3.cursor()
cursor3.execute("""DROP TABLE IF EXISTS screener_results""")
screener_results.to_sql('screener_results', conn3, if_exists='replace', index=False)

conn1.close()
conn2.close()
conn3.close()