import pandas as pd
from dotenv import load_dotenv
from src import fiscal_years, stock_list, market_cap, financial_statements, pb_ratio
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
for stock in test_stocks:
    # Get balance sheet from financial modeling prep
    balance_sheet = financial_statements.get_balance_sheet(t=stock, key=fmp_api_key)
    # Calculate market cap
    mc = market_cap.calc_market_cap(t=stock, balance=balance_sheet)
    market_caps_list.append(mc)
    # Get shareholder equity
    shareholder_equity = pb_ratio.get_shareholder_equity(balance=balance_sheet)
    shareholder_equity_list.append(shareholder_equity)
    # Get fiscal years to add to the dataframe in the final step

market_cap_dict = dict(zip(test_stocks, market_caps_list))
df_market_cap = pd.DataFrame.from_dict(market_cap_dict)
shareholder_equity_dict = dict(zip(test_stocks, shareholder_equity_list))
df_shareholder_equity = pd.DataFrame.from_dict(shareholder_equity_dict)

# Calculate PB Ratio
df_pb_ratio = pb_ratio.calc_pb_ratio(market_cap=df_market_cap, shareholder_equity=df_shareholder_equity)

# Obtain fiscal years
fiscal_years_list = fiscal_years.get_fiscal_years(balance=balance_sheet)
df_pb_ratio.insert(loc=0, column='Fiscal Years', value=fiscal_years_list)
