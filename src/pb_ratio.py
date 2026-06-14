def get_shareholder_equity(balance):
    share_holder_equity = []
    for year in balance:
        equity = year['totalStockholdersEquity']
        share_holder_equity.append(equity)

    return share_holder_equity

def calc_pb_ratio(market_cap, shareholder_equity):
    pb_ratio = round(market_cap / shareholder_equity, 2)
    return pb_ratio
