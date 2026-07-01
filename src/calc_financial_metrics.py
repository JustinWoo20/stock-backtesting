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

de_ratio_list = []
gross_profit_margin_list = []
net_income_growth_list = []
pb_ratio_list = []
revenue_growth_list = []
shareholders_list = []
z_score_list = []

for stock in test_stocks:
    # Obtain necessary financial statements
    income_statement = financial_statements.get_income_statement(t=stock, key=fmp_api_key)
    balance_sheet = financial_statements.get_balance_sheet(t=stock, key=fmp_api_key)
    income_growth_stat = financial_statements.get_income_growth(t=stock, key=fmp_api_key)
    financial_ratios_stat = financial_statements.get_financial_ratios(t=stock, key=fmp_api_key)
    key_metrics_stat = financial_statements.get_key_metrics(t=stock, key=fmp_api_key)
    # Obtain data from financial statements
    # Current Assets for z-score
    current_assets = statement_data.get_current_assets(balance=balance_sheet)
    # Current liabilities for z-score
    current_liabilities = statement_data.get_current_liabilities(balance=balance_sheet)
    # D/E Ratio
    de_ratio = statement_data.get_de_ratio(fr=financial_ratios_stat)
    de_ratio_list.append(de_ratio)
    # ebit for z-score
    ebit = statement_data.get_ebit(income=income_statement)
    # Gross Profit Margins
    gpm = statement_data.get_gross_profit_margin(fr=financial_ratios_stat)
    gross_profit_margin_list.append(gpm)
    # Market Cap for z score and pb ratio
    mc = statement_data.get_market_cap(km=key_metrics_stat)
    # Net Income Growth
    nig = statement_data.get_net_income_growth(growth=income_growth_stat)
    net_income_growth_list.append(nig)
    # P/B Ratio
    pb_ratio = statement_data.get_pb_ratio(financial_ratios_stat)
    pb_ratio_list.append(pb_ratio)
    # Retained Earnings for z-score
    retained_earnings = statement_data.get_retained_earnings(balance=balance_sheet)
    # Revenue Growth
    revenue_growth = statement_data.get_revenue_growth(growth=income_growth_stat)
    revenue_growth_list.append(revenue_growth)
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
        z_score_list.append(z_score)

    else:
        z_score = altman_z_score.calc_zscore_manufacturing(ta=total_assets, ca=current_assets, tl=total_liabilities,
                                                 cl=current_liabilities, re=retained_earnings, ebit=ebit, s=sales,
                                                 cap=mc)
        z_score_list.append(z_score)

# Get fiscal years
f_years = fiscal_years.get_fiscal_years(balance=financial_statements.get_balance_sheet(t=test_stocks[0], key=fmp_api_key))

# Create dictionaries
de_ratio_dict = dict(zip(test_stocks, de_ratio_list))
gross_profit_margin_dict = dict(zip(test_stocks, gross_profit_margin_list))
net_income_growth_dict = dict(zip(test_stocks, net_income_growth_list))
pb_ratio_dict = dict(zip(test_stocks, pb_ratio_list))
revenue_growth_dict = dict(zip(test_stocks, revenue_growth_list))
z_score_dict = dict(zip(test_stocks, z_score_list))

# # Create dataframes
df_de_ratio = pd.DataFrame.from_dict(de_ratio_dict)
df_gpm = pd.DataFrame.from_dict(gross_profit_margin_dict)
df_net_income_growth = pd.DataFrame.from_dict(net_income_growth_dict)
df_pb_ratio = pd.DataFrame.from_dict(pb_ratio_dict)
df_revenue_growth = pd.DataFrame.from_dict(revenue_growth_dict)
df_z_score = pd.DataFrame.from_dict(z_score_dict)

dataframes = {'de_ratio': df_de_ratio,
              'gpm': df_gpm,
              'net_income_growth': df_net_income_growth,
              'pb_ratio': df_pb_ratio,
              'revenue_growth': df_revenue_growth,
              'altman_z_score': df_z_score}

for df in dataframes.values():
    df.insert(loc=0, column='Fiscal Years', value=f_years)

conn = sql.connect("../data/financial_metrics.db")
cursor = conn.cursor()

for name, df in dataframes.items():
    cursor.execute(f"DROP TABLE IF EXISTS {name}")
    df.to_sql(name, conn, if_exists='replace', index=False)

conn.close()
