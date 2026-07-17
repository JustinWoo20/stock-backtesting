def get_fiscal_years(balance):
    fiscal_years = []
    for year in balance:
        fiscal_year = year['fiscalYear']
        fiscal_years.append(fiscal_year)

    return fiscal_years

def get_filing_dates(balance):
    filing_dates = []
    for year in balance:
        filing_date = year['filingDate']
        filing_dates.append(filing_date)

    return filing_dates