def get_current_assets(balance):
    current_assets = []
    for year in balance:
        current_asset = year['totalCurrentAssets']
        current_assets.append(current_asset)

    return current_assets

def get_current_liabilities(balance):
    current_liabilities = []
    for year in balance:
        current_liability = year['totalCurrentLiabilities']
        current_liabilities.append(current_liability)

    return current_liabilities

def get_de_ratio(fr):
    de_ratio = []
    for year in fr:
        de = year['debtToEquityRatio']
        de_ratio.append(de)

    return de_ratio

def get_ebit(income):
    ebit_ = []
    for year in income:
        ebit = year['ebit']
        ebit_.append(ebit)

    return ebit_

def get_gross_profit_margin(fr):
    gross_profit_margin = []
    for year in fr:
        gpm = year['grossProfitMargin']
        gross_profit_margin.append(gpm)

    return gross_profit_margin

def get_market_cap(km):
    market_cap = []
    for year in km:
        m = year['marketCap']
        market_cap.append(m)

    return market_cap

def get_net_income_growth(growth):
    net_income_growth = []
    for year in growth:
        growth = year['growthNetIncome']
        net_income_growth.append(growth)

    return net_income_growth

def get_pb_ratio(fr):
    pb_list = []
    for year in fr:
        pb = year['priceToBookRatio']
        pb_list.append(pb)

    return pb_list

def get_retained_earnings(balance):
    retained_earnings_list = []
    for year in balance:
        retained_earnings = year['retainedEarnings']
        retained_earnings_list.append(retained_earnings)

    return retained_earnings_list

def get_revenue_growth(growth):
    revenue_growth = []
    for year in growth:
        growth = year['growthRevenue']
        revenue_growth.append(growth)

    return revenue_growth

def get_sales(income):
    sales = []
    for year in income:
        s = year['revenue']
        sales.append(s)

    return sales

def get_shareholder_equity(balance):
    shareholder_equity = []
    for year in balance:
        equity = year['totalStockholdersEquity']
        shareholder_equity.append(equity)

    return shareholder_equity

def get_total_assets(balance):
    total_assets = []
    for year in balance:
        ta = year['totalAssets']
        total_assets.append(ta)

    return total_assets

def get_total_debt(balance):
    total_debt = []
    for year in balance:
        debt = year['totalDebt']
        total_debt.append(debt)

    return total_debt

def get_total_liabilities(balance):
    total_liabilities = []
    for year in balance:
        tl = year['totalLiabilities']
        total_liabilities.append(tl)

    return total_liabilities

