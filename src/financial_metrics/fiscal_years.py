from datetime import datetime

def get_fiscal_years(balance):
    fiscal_years = []
    for year in balance:
        fiscal_year = year['fiscalYear']
        fiscal_year = int(fiscal_year)
        fiscal_years.append(fiscal_year)

    return fiscal_years

def get_filing_dates(balance):
    filing_dates = []
    for year in balance:
        filing_date = year['filingDate']
        filing_date = datetime.strptime(filing_date, "%Y-%m-%d").date()
        filing_dates.append(filing_date)

    return filing_dates