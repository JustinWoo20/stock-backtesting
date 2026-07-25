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
    SELECT DISTINCT fiscal_years
    FROM financial_metrics""", conn1)
years = list(years['fiscal_years'])

def query_financial_metrics(conn):
    query = "SELECT * FROM financial_metrics;"
    df_financial_metrics = pd.read_sql_query(query, conn)
    return df_financial_metrics
df_fm = query_financial_metrics(conn1)

def query_industry_averages(conn):
    query = "SELECT * FROM industries;"
    df_industry_averages = pd.read_sql_query(query, conn)
    return df_industry_averages
df_ia = query_industry_averages(conn2)

def get_company_value(metric_name, data, ticker, year):
    # Query financial metrics database to find a company's respective value
    query_row = data.loc[(data['fiscal_years'] == year) &
                         (data['stocks'] == ticker) &
                         (data['key_metrics'] == metric_name)]
    metric_value = query_row['value']
    if len(metric_value) == 1:
        return metric_value.iloc[0]
    raise ValueError(
        f"Expected 1 row for {metric_name}/{ticker}/{year}, got {len(query_row)}")

def get_industry_value(metric_name, industry, data):
    # Query the industry averages db to find the average value for a company's industry
    query_row = data.loc[data['Industry'] == industry]
    industry_average = query_row[metric_name]
    if len(industry_average) == 1:
        return industry_average.iloc[0]
    raise ValueError(
        f"Expected 1 row for {metric_name}/{industry}, got {len(query_row)}")

def compare_z_score(finance_data, ticker, year):
    company_value = get_company_value(metric_name='altman_z_score', data=finance_data, ticker=ticker, year=year)
    if company_value >= 3:
        return 2
    elif company_value >= 2:
        return 1
    return 0

def compare_gpm(finance_data, industry_data, ticker, year, ind):
    company_value = get_company_value(metric_name='gpm', data=finance_data, ticker=ticker, year=year)
    industry_value = get_industry_value(metric_name='gpm', industry=ind, data=industry_data)
    if company_value > industry_value:
        return 1
    return 0

def compare_pb_ratio(finance_data, industry_data, ticker, year, ind):
    company_value = get_company_value(metric_name='pb_ratio', data=finance_data, ticker=ticker, year=year)
    industry_value = get_industry_value(metric_name='pb_ratio', industry=ind, data=industry_data)
    if company_value > industry_value:
        return 1
    return 0

def compare_de_ratio(finance_data, industry_data, ticker, year, ind):
    company_value = get_company_value(metric_name='de_ratio', data=finance_data, ticker=ticker, year=year)
    industry_value = get_industry_value(metric_name='de_ratio', industry=ind, data=industry_data)
    if company_value > industry_value:
        return 1
    return 0

def compare_net_income_growth(finance_data, ticker, year):
    company_value = get_company_value(metric_name='net_income_growth', data=finance_data, ticker=ticker, year=year)
    if company_value > 0:
        return 1
    return 0

def compare_revenue_growth(finance_data, industry_data, ticker, year, ind):
    company_value = get_company_value(metric_name='revenue_growth', data=finance_data, ticker=ticker, year=year)
    industry_value = get_industry_value(metric_name='revenue_growth', industry=ind, data=industry_data)
    if company_value > industry_value:
        return 1
    return 0

def get_filing_dates(year, finance_data, ticker):
    query_row = finance_data.loc[(finance_data['fiscal_years'] == year) &
                         (finance_data['stocks'] == ticker) &
                         (finance_data['key_metrics'] == 'de_ratio')]
    fd = query_row['filing_date'].iloc[0]
    return fd

rows = []

for stock, industry in ind_dict.items():
    for year in years:
        total_points = 0
        z_score_points = compare_z_score(finance_data=df_fm, ticker=stock, year=year)
        total_points += z_score_points
        gpm_points = compare_gpm(finance_data=df_fm, industry_data=df_ia, ticker=stock, year=year, ind=industry)
        total_points += gpm_points
        pb_points = compare_pb_ratio(finance_data=df_fm, industry_data=df_ia, ticker=stock, year=year, ind=industry)
        total_points += pb_points
        de_points = compare_de_ratio(finance_data=df_fm, industry_data=df_ia, ticker=stock, year=year, ind=industry)
        total_points += de_points
        ni_growth_points = compare_net_income_growth(finance_data=df_fm, ticker=stock, year=year)
        total_points += ni_growth_points
        rev_growth_points = compare_revenue_growth(finance_data=df_fm, industry_data=df_ia, ticker=stock, year=year, ind=industry)
        total_points += rev_growth_points
        file_date = get_filing_dates(year=year, finance_data=df_fm, ticker=stock)
        rows_to_add = {
            'fiscal_years': year,
            'filing_date': file_date,
            'stocks': stock,
            'result': total_points,
        }
        rows.append(rows_to_add)

df_results = pd.DataFrame(data=rows, columns=['fiscal_years', 'filing_date', 'stocks', 'result'])
conn3 = sql.connect("../data/screener_results.db")
cursor3 = conn3.cursor()
cursor3.execute("""DROP TABLE IF EXISTS screener_results""")
df_results.to_sql('screener_results', conn3, if_exists='replace', index=False)

conn1.close()
conn2.close()
conn3.close()