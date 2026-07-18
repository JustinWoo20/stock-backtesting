from dotenv import load_dotenv
import pandas as pd
import os
import sqlite3 as sql
from financial_metrics import altman_z_score
from financial_metrics import financial_statements
from financial_metrics import fiscal_years
from financial_metrics import statement_data

load_dotenv()
fmp_api_key = os.getenv('FMP_API_KEY')

test_stocks = ['AAPL', 'TSLA', 'AMZN']
software_ind = ['Software - Application', 'Internet Content & Information',]

column_names = ['fiscal_years', 'filing_date', 'stocks', 'key_metrics', 'value']
df_financial_metrics = pd.DataFrame(columns=column_names)

stock_column = []
metrics_column = []

for stock in test_stocks:
    # Obtain necessary financial statements
    income_statement = financial_statements.get_income_statement(t=stock, key=fmp_api_key)
    balance_sheet = financial_statements.get_balance_sheet(t=stock, key=fmp_api_key)
    income_growth_stat = financial_statements.get_income_growth(t=stock, key=fmp_api_key)
    financial_ratios_stat = financial_statements.get_financial_ratios(t=stock, key=fmp_api_key)
    key_metrics_stat = financial_statements.get_key_metrics(t=stock, key=fmp_api_key)
    # Get fiscal years
    f_years = fiscal_years.get_fiscal_years(balance=balance_sheet)
    # Get filing dates
    file_date = fiscal_years.get_filing_dates(balance=balance_sheet)
    # Insert stock ticker into stock_column list
    for x in range(0, 5):
        stock_column.append(stock)
    # Obtain data from financial statements
    # Current Assets for z-score
    current_assets = statement_data.get_current_assets(balance=balance_sheet)

    # Current liabilities for z-score
    current_liabilities = statement_data.get_current_liabilities(balance=balance_sheet)

    # D/E Ratio
    de_ratio = statement_data.get_de_ratio(fr=financial_ratios_stat)
    for x in range(0,5):
        metrics_column.append('de_ratio') # append metric name 5 times
    new_data = [f_years, file_date, stock_column, metrics_column, de_ratio]
    new_rows = dict(zip(column_names, new_data)) # Zip column names and new data  to concat to dataframe
    df_new_rows = pd.DataFrame.from_dict(new_rows,)
    df_financial_metrics = pd.concat([df_financial_metrics, df_new_rows], ignore_index=True)
    # Clear values and metric names
    metrics_column.clear()

    # ebit for z-score
    ebit = statement_data.get_ebit(income=income_statement)

    # Gross Profit Margins
    gpm = statement_data.get_gross_profit_margin(fr=financial_ratios_stat)
    for x in range(0,5):
       metrics_column.append('gpm')
    new_data = [f_years, file_date, stock_column, metrics_column, gpm]
    new_rows = dict(zip(column_names, new_data))
    df_new_rows = pd.DataFrame.from_dict(new_rows,)
    df_financial_metrics = pd.concat([df_financial_metrics, df_new_rows], ignore_index=True)
    metrics_column.clear()

    # Market Cap for z score and pb ratio
    mc = statement_data.get_market_cap(km=key_metrics_stat)

    # Net Income Growth
    nig = statement_data.get_net_income_growth(growth=income_growth_stat)
    for x in range(0,5):
        metrics_column.append('net_income_growth')
    new_data = [f_years, file_date, stock_column, metrics_column, nig]
    new_rows = dict(zip(column_names, new_data))
    df_new_rows = pd.DataFrame.from_dict(new_rows,)
    df_financial_metrics = pd.concat([df_financial_metrics, df_new_rows], ignore_index=True)
    metrics_column.clear()

    # P/B Ratio
    pb_ratio = statement_data.get_pb_ratio(financial_ratios_stat)
    for x in range(0,5):
        metrics_column.append('pb_ratio')
    new_data = [f_years, file_date, stock_column, metrics_column, pb_ratio]
    new_rows = dict(zip(column_names, new_data))
    df_new_rows = pd.DataFrame.from_dict(new_rows,)
    df_financial_metrics = pd.concat([df_financial_metrics, df_new_rows], ignore_index=True)
    metrics_column.clear()

    # Retained Earnings for z-score
    retained_earnings = statement_data.get_retained_earnings(balance=balance_sheet)

    # Revenue Growth
    revenue_growth = statement_data.get_revenue_growth(growth=income_growth_stat)
    for x in range(0,5):
        metrics_column.append('revenue_growth')
    new_data = [f_years, file_date, stock_column, metrics_column, revenue_growth]
    new_rows = dict(zip(column_names, new_data))
    df_new_rows = pd.DataFrame.from_dict(new_rows,)
    df_financial_metrics = pd.concat([df_financial_metrics, df_new_rows], ignore_index=True)
    metrics_column.clear()

    # Sales (revenue) for z-score
    sales = statement_data.get_sales(income=income_statement)

    # Shareholders equity for z-score
    se = statement_data.get_shareholder_equity(balance=balance_sheet)

    # Total assets for z-score
    total_assets = statement_data.get_total_assets(balance=balance_sheet)

    # Total liabilities for z-score
    total_liabilities = statement_data.get_total_liabilities(balance=balance_sheet)

    # Obtain company industry
    ind = altman_z_score.get_industry(ticker=stock)
    if ind in software_ind:
        z_score = altman_z_score.calc_zscore_nonmanufacturing(ta=total_assets, ca=current_assets, tl=total_liabilities,
                                                              cl=current_liabilities, re=retained_earnings, ebit=ebit,
                                                              sh=se)

    else:
        z_score = altman_z_score.calc_zscore_manufacturing(ta=total_assets, ca=current_assets, tl=total_liabilities,
                                                 cl=current_liabilities, re=retained_earnings, ebit=ebit, s=sales,
                                                 cap=mc)


    for x in range(0,5):
        metrics_column.append('altman_z_score')
    new_data = [f_years, file_date, stock_column, metrics_column, z_score]
    new_rows = dict(zip(column_names, new_data))
    df_new_rows = pd.DataFrame.from_dict(new_rows,)
    df_financial_metrics = pd.concat([df_financial_metrics, df_new_rows], ignore_index=True)
    stock_column.clear()
    metrics_column.clear()

df_fm_sorted = df_financial_metrics.sort_values(by=['stocks', 'fiscal_years', 'key_metrics'])

conn = sql.connect("../data/financial_metrics.db")
cursor = conn.cursor()

cursor.execute(f"DROP TABLE IF EXISTS financial_metrics")
df_fm_sorted.to_sql('financial_metrics', conn, if_exists='replace', index=False)

conn.close()
