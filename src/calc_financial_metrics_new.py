from dotenv import load_dotenv
import pandas as pd
import os
from financial_metrics import altman_z_score
from financial_metrics import financial_statements
from financial_metrics import statement_data

load_dotenv()

fmp_api_key = os.getenv('FMP_API_KEY')

test_stocks = ['AAPL', 'TSLA', 'AMZN']
software_ind = ['Software - Application', 'Internet Content & Information',]
# Manufacturing calculations
# Altman Z-Score = 1.2A + 1.4B + 3.3C + 0.6D + 1.0E
# Where:
# A = working capital (current assets - current liabilities) / total assets
# B = retained earnings / total assets
# C = earnings before interest and tax / total assets
# D = market value of equity / total liabilities
# E = sales / total assets

# current_assets_list = []
# current_liabilities_list = []
# ebit_list = []
de_ratio_list = []
gross_profit_margin_list = []
# market_cap_list = []
pb_ratio_list = []
# retained_earnings_list = []
# sales_list = []
shareholders_list = []
# total_assets_list = []
# total_debt_list = []
# total_liabilities_list = []
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
    # current_assets_list.append(current_assets)
    # Current liabilities for z-score
    current_liabilities = statement_data.get_current_liabilities(balance=balance_sheet)
    # current_liabilities_list.append(current_liabilities)
    # D/E Ratio
    de_ratio = statement_data.get_de_ratio(fr=financial_ratios_stat)
    de_ratio_list.append(de_ratio)
    # ebit for z-score
    ebit = statement_data.get_ebit(income=income_statement)
    # ebit_list.append(ebit)
    # Gross Profit Margins
    gpm = statement_data.get_gross_profit_margin(fr=financial_ratios_stat)
    gross_profit_margin_list.append(gpm)
    # Market Cap for z score and pb ratio
    mc = statement_data.get_market_cap(km=key_metrics_stat)
    # market_cap_list.append(mc)
    # P/B Ratio
    pb_ratio = statement_data.get_pb_ratio(financial_ratios_stat)
    pb_ratio_list.append(pb_ratio)
    # Retained Earnings for z-score
    retained_earnings = statement_data.get_retained_earnings(balance=balance_sheet)
    # retained_earnings_list.append(retained_earnings)
    # Sales (revenue) for z-score
    sales = statement_data.get_sales(income=income_statement)
    # sales_list.append(sales)
    # Shareholders equity for z-score, pb ratio, and de ratio
    se = statement_data.get_shareholder_equity(balance=balance_sheet)
    shareholders_list.append(se)
    # Total assets for z-score
    total_assets = statement_data.get_total_assets(balance=balance_sheet)
    # total_assets_list.append(total_assets)
    # Total debt for de ratio
    td = statement_data.get_total_debt(balance=balance_sheet)
    # total_debt_list.append(td)
    # Total liabilities for z-score
    total_liabilities = statement_data.get_total_liabilities(balance=balance_sheet)
    #total_liabilities_list.append(total_liabilities)
    # Obtain company industry
    ind = altman_z_score.get_industry(ticker=stock, industry_list=software_ind)
    if ind:
        z_score = altman_z_score.calc_zscore_manufacturing(ta=total_assets, ca=current_assets, tl=total_liabilities,
                                                 cl=current_liabilities, re=retained_earnings, ebit=ebit, s=sales,
                                                 cap=mc)
        z_score_list.append(z_score)
    else:
        z_score = altman_z_score.calc_zscore_nonmanufacturing(ta=total_assets, ca=current_assets, tl=total_liabilities,
                                                              cl=current_liabilities, re=retained_earnings, ebit=ebit,
                                                              sh=se)
        z_score_list.append(z_score)


# Create dictionaries
# current_assets_dict = dict(zip(test_stocks, current_assets_list))
# current_liabilities_dict = dict(zip(test_stocks, current_liabilities_list))
de_ratio_dict = dict(zip(test_stocks, de_ratio_list))
# ebit_dict = dict(zip(test_stocks, ebit_list))
# gross_profit_margin_dict = dict(zip(test_stocks, gross_profit_margin_list))
# market_cap_dict = dict(zip(test_stocks, market_cap_list))
pb_ratio_dict = dict(zip(test_stocks, pb_ratio_list))
# retained_earnings_dict = dict(zip(test_stocks, retained_earnings_list))
# sales_dict = dict(zip(test_stocks, sales_list))
# shareholders_dict = dict(zip(test_stocks, shareholders_list))
# total_assets_dict = dict(zip(test_stocks, total_assets_list))
# total_debt_dict = dict(zip(test_stocks, total_debt_list))
# total_liabilities_dict = dict(zip(test_stocks, total_liabilities_list))
z_score_dict = dict(zip(test_stocks, z_score_list))

# # Create dataframes
# df_current_assets = pd.DataFrame.from_dict(current_assets_dict)
# df_current_liabilities = pd.DataFrame.from_dict(current_liabilities_dict)
df_de_ratio = pd.DataFrame.from_dict(de_ratio_dict)
# df_ebit = pd.DataFrame.from_dict(ebit_dict)
# df_gpm = pd.DataFrame.from_dict(gross_profit_margin_dict)
# df_market_cap = pd.DataFrame.from_dict(market_cap_dict)
df_pb_ratio = pd.DataFrame.from_dict(pb_ratio_dict)
# df_retained_earnings = pd.DataFrame.from_dict(retained_earnings_dict)
# df_sales = pd.DataFrame.from_dict(sales_dict)
# df_shareholders = pd.DataFrame.from_dict(shareholders_dict)
# df_total_assets = pd.DataFrame.from_dict(total_assets_dict)
# df_total_debt = pd.DataFrame.from_dict(total_debt_dict)
# df_total_liabilities = pd.DataFrame.from_dict(total_liabilities_dict)
df_z_score = pd.DataFrame.from_dict(z_score_dict)


# D/E Ratio
# Gross Profit Margin
# P/B Ratio
# Revenue Growth


