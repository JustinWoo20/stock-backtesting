def get_total_debt(balance):
    total_debts = []
    for year in balance:
        total_debt = year['totalDebt']
        total_debts.append(total_debt)

    return total_debts

def calc_de_ratio(debt, shareholder_equity):
    df_de_ratio = round(debt / shareholder_equity, 2)

    return df_de_ratio