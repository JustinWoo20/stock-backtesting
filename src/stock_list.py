def stock_list(tickers):
    tickers_split = tickers.split(',')
    symbols_list = [s.strip() for s in tickers_split]
    return symbols_list
