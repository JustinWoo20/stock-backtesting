import pandas as pd
from dotenv import load_dotenv
from src import (fiscal_years, stock_list, market_cap, financial_statements, pb_ratio, de_ratio, revenue_growth,
                 altman_z_score, gross_profit_margin)
import os

load_dotenv()

fmp_api_key = os.getenv('FMP_API_KEY')

# Stocks that can be tested using financial modeling
# symbols_string = ("AAPL, TSLA, AMZN, MSFT, NVDA, GOOGL, META, NFLX, JPM, V, BAC, PYPL, DIS, T, PFE, COST, INTC, "
#                   "KO, TGT, NKE, BA, BABA, XOM, WMT, GE, CSCO, VZ, JNJ, CVX, PLTR, SQ, SHOP, SBUX, SOFI, HOOD, "
#                   "RBLX, SNAP, AMD, UBER, FDX, ABBV, ETSY, MRNA, LMT, GM, F, LCID, CCL, DAL, UAL, AAL, TSM, SONY, ET, "
#                   "MRO, COIN, RIVN, RIOT, CPRX, NOK, ROKU, VIAC, ATVI, BIDU, DOCU, ZM, PINS, TLRY, WBA, MGM, NIO, "
#                   "C, GS, WFC, ADBE, PEP, UNH, CARR, HCA, TWTR, BILI, SIRI, FUBO, RKT")
#
#
# stocks = stock_list.stock_list(tickers=symbols_string)

test_stocks = ['AAPL', 'TSLA', 'AMZN']

# Find market cap and shareholder equity to calculate PB ratio
market_caps_list = []
shareholder_equity_list = []
total_debt_list = []
revenue_growth_list = []
gross_profit_margin_list = []
for stock in test_stocks:
    # Get necessary financial statements from financial modeling prep
    income_statement = financial_statements.get_income_statement(t=stock, key=fmp_api_key)
    balance_sheet = financial_statements.get_balance_sheet(t=stock, key=fmp_api_key)
    income_growth_stat = financial_statements.get_income_growth(t=stock, key=fmp_api_key)
    # Calculate market cap
    mc = market_cap.calc_market_cap(t=stock, balance=balance_sheet)
    market_caps_list.append(mc)
    # Get shareholder equity
    shareholder_equity = pb_ratio.get_shareholder_equity(balance=balance_sheet)
    shareholder_equity_list.append(shareholder_equity)
    # Get yearly total debt
    total_debt = de_ratio.get_total_debt(balance=balance_sheet)
    total_debt_list.append(total_debt)
    # Get revenue growth
    rg = revenue_growth.calc_revenue_growth(income_growth=income_growth_stat)
    revenue_growth_list.append(rg)
    # Calculate gross profit margins
    gpm = gross_profit_margin.calc_gross_profit_margin(income=income_statement)
    gross_profit_margin_list.append(gpm)

# Create pandas dataframes from various metrics
market_cap_dict = dict(zip(test_stocks, market_caps_list))
df_market_cap = pd.DataFrame.from_dict(market_cap_dict)

shareholder_equity_dict = dict(zip(test_stocks, shareholder_equity_list))
df_shareholder_equity = pd.DataFrame.from_dict(shareholder_equity_dict)

total_debt_dict = dict(zip(test_stocks, total_debt_list))
df_total_debt = pd.DataFrame.from_dict(total_debt_dict)

revenue_growth_dict = dict(zip(test_stocks, revenue_growth_list))
df_revenue_growth = pd.DataFrame.from_dict(revenue_growth_dict)

gross_profit_margin_dict = dict(zip(test_stocks, gross_profit_margin_list))
df_gross_profit_margin = pd.DataFrame.from_dict(gross_profit_margin_dict)

# Calculate PB Ratio
df_pb_ratio = pb_ratio.calc_pb_ratio(market_cap=df_market_cap, shareholder_equity=df_shareholder_equity)

# Calculate DE Ratio
df_de_ratio = de_ratio.calc_de_ratio(debt=df_total_debt, shareholder_equity=df_shareholder_equity)

# Obtain fiscal years
fiscal_years_list = fiscal_years.get_fiscal_years(balance=balance_sheet)
df_pb_ratio.insert(loc=0, column='Fiscal Years', value=fiscal_years_list)
df_de_ratio.insert(loc=0, column='Fiscal Years', value=fiscal_years_list)
df_revenue_growth.insert(loc=0, column='Fiscal Years', value=fiscal_years_list)
df_gross_profit_margin.insert(loc=0, column='Fiscal Years', value=fiscal_years_list)

# Add altman z score
