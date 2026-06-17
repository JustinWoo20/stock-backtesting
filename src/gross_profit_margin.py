def calc_gross_profit_margin(income):
    gross_profit_margin = []
    for year in income:
        total_revenue = year['revenue']
        gross_profit = year['grossProfit']
        gpm = round(gross_profit / total_revenue, 2)
        gross_profit_margin.append(gpm)

    return gross_profit_margin