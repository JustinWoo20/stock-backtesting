def get_fiscal_years(balance):
    fiscal_years = []
    for year in balance:
        fiscal_year = year['fiscalYear']
        fiscal_years.append(fiscal_year)

    return fiscal_years
