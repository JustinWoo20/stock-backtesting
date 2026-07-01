import numpy as np
import yfinance as yf

def get_industry(ticker):
    # Obtain company industry to determine if manufacturing or non-manufacturing
    yf_ticker = yf.Ticker(ticker)
    info = yf_ticker.info
    comp_industry = info['industry']
    return comp_industry

# Manufacturing calculations
# Altman Z-Score = 1.2A + 1.4B + 3.3C + 0.6D + 1.0E
# Where:
# A = working capital (current assets - current liabilities) / total assets
# B = retained earnings / total assets
# C = earnings before interest and tax / total assets
# D = market value of equity / total liabilities
# E = sales / total assets

def calc_zscore_manufacturing(ta, ca, tl, cl, re, ebit, s, cap):
    # Calculates the Altman Z-Score for manufacturing companies
    working_capital = np.array(ca) - np.array(cl)
    a = working_capital / np.array(ta)
    a *= 1.2
    b = np.array(re) / np.array(ta)
    b *= 1.4
    c = np.array(ebit) / np.array(ta)
    c *= 3.3
    d = np.array(cap) / np.array(tl)
    d *= .6
    e = np.array(s )/ np.array(ta)

    z_score = (a+b+c+d+e)

    return z_score


# Non-manufacturing calculations
# Altman Z-Score = 6.56X1 + 3.26X2 + 6.72X3 + 1.05X4
# X1 = working capital (current assets − current liabilities) / total assets
# X2 = retained earnings / total assets
# X3 = earnings before interest and taxes / total assets
# X4 = book value of equity / total liabilities

def calc_zscore_nonmanufacturing(ta, ca, tl, cl, re, ebit, sh):
    # Calculates the Altman Z-Score for non-manufacturing companies
    working_capital = np.array(ca) - np.array(cl)
    a = working_capital / np.array(ta)
    a *=6.56
    b = np.array(re) / np.array(ta)
    b *= 3.26
    c = np.array(ebit) / np.array(ta)
    c *= 6.72
    d = np.array(sh) / np.array(tl)

    z_score = a + b + c + d
    return z_score
