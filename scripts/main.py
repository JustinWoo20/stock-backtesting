import pandas as pd
from dotenv import load_dotenv
from src import stock_list, market_cap, financial_statements
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

market_caps_list = []
for stock in test_stocks:
    # Get balance sheet from financial modeling prep
    balance_sheet = financial_statements.get_balance_sheet(t=stock, key=fmp_api_key)
    # Calculate market cap
    mc = market_cap.calc_market_cap(t=stock, balance=balance_sheet)
    market_caps_list.append(mc)
market_cap_dict = dict(zip(test_stocks, market_caps_list))
df_market_cap = pd.DataFrame.from_dict(market_cap_dict)

#


