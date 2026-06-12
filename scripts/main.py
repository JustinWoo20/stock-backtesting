from src import stock_list, market_cap

# symbols_string = ("AAPL, TSLA, AMZN, MSFT, NVDA, GOOGL, META, NFLX, JPM, V, BAC, PYPL, DIS, T, PFE, COST, INTC, "
#                   "KO, TGT, NKE, BA, BABA, XOM, WMT, GE, CSCO, VZ, JNJ, CVX, PLTR, SQ, SHOP, SBUX, SOFI, HOOD, "
#                   "RBLX, SNAP, AMD, UBER, FDX, ABBV, ETSY, MRNA, LMT, GM, F, LCID, CCL, DAL, UAL, AAL, TSM, SONY, ET, "
#                   "MRO, COIN, RIVN, RIOT, CPRX, NOK, ROKU, VIAC, ATVI, BIDU, DOCU, ZM, PINS, TLRY, WBA, MGM, NIO, "
#                   "C, GS, WFC, ADBE, PEP, UNH, CARR, HCA, TWTR, BILI, SIRI, FUBO, RKT")
#
#
# stocks = stock_list.stock_list(tickers=symbols_string)

test_stocks = ['AAPL', 'TSLA', 'AMZN']

for stock in test_stocks:
    ticker = market_cap.get_yfinance_ticker(t=stock)
    price_history = market_cap.yfinance_historic_price(t=ticker)
    shares_history = market_cap.yfinance_get_shares(t=ticker)
    mc = market_cap.calc_market_cap()
