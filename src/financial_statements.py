import requests

def get_income_statement(t, key):
    # This function will return the income statement, balance sheet, and cash flow statement of a company
    income_endpoint = f"https://financialmodelingprep.com/stable/income-statement?symbol={t}&apikey={key}"
    income_requests = requests.get(income_endpoint)
    income_data = income_requests.json()
    return income_data

def get_balance_sheet(t, key):
    balance_endpoint = f"https://financialmodelingprep.com/stable/balance-sheet-statement?symbol={t}&apikey={key}"
    balance_requests = requests.get(balance_endpoint)
    balance_data = balance_requests.json()
    return balance_data

def get_cash_flow_statement(t, key):
    cash_endpoint = f"https://financialmodelingprep.com/stable/cash-flow-statement?symbol={t}&apikey={key}"
    cash_requests = requests.get(cash_endpoint)
    cash_data = cash_requests.json()
    return cash_data

def get_income_growth(t, key):
    income_growth_endpoint = f"https://financialmodelingprep.com/stable/income-statement-growth?symbol={t}&apikey={key}"
    income_growth_requests = requests.get(income_growth_endpoint)
    income_growth_data = income_growth_requests.json()
    return income_growth_data
