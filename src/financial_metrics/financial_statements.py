import requests

# These functions will return a company's income statement, balance sheet, cash flow statement, and income growth

def get_income_statement(t, key):
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

def get_financial_ratios(t, key):
    financial_ratios_endpoint = f"https://financialmodelingprep.com/stable/ratios?symbol={t}&apikey={key}"
    financial_ratios_requests = requests.get(financial_ratios_endpoint)
    financial_ratios_data = financial_ratios_requests.json()
    return financial_ratios_data

def get_key_metrics(t, key):
    key_metrics_endpoint = f"https://financialmodelingprep.com/stable/key-metrics?symbol={t}&apikey={key}"
    financial_metrics_requests = requests.get(key_metrics_endpoint)
    financial_metrics_data = financial_metrics_requests.json()
    return financial_metrics_data
