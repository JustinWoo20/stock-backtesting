def calc_revenue_growth(income_growth):
    revenue_growth = []
    for year in income_growth:
        growth = year['growthRevenue']
        revenue_growth.append(growth)

    return revenue_growth