import pandas as pd
import yfinance as yf

def get_yfinance_ticker(t):
    yfinance_ticker = yf.Ticker(t)
    return yfinance_ticker

def yfinance_historic_price(t):
    # Returns the historic stock prices of a stock
    price_history = t.history('5y')
    price_history = price_history.reset_index()

    return price_history

def yfinance_get_shares(t):
    # Returns the historical data for number of shares
    shares = t.get_shares_full(start='2021-10-01')
    df_shares = pd.DataFrame(data=shares,  index=None,)
    df_shares.reset_index(inplace=True)
    df_shares = df_shares.rename(columns={'index': 'Date', 0: 'Shares'})
    df_shares['Date'] = pd.to_datetime(df_shares['Date']).dt.date

    return df_shares


def calc_market_cap(t, balance):
    market_caps = []

    for year in balance:
        # Find filing date
        file_date = year['filingDate']
        # Get yfinance object
        yfinance_ticker = get_yfinance_ticker(t)

        # Find price on filing date
        price_history = yfinance_historic_price(t=yfinance_ticker)
        filing_date_stock_price = price_history[price_history['Date'] == file_date]

        # Convert file date to datetime for next step
        file_date = pd.to_datetime(file_date)
        # Find closest date on shares df
        shares_history = yfinance_get_shares(t=yfinance_ticker)
        shares_history['Date'] = pd.to_datetime(shares_history['Date'])
        closest_date = (shares_history['Date'] - file_date).abs().idxmin()
        closest_row = shares_history.loc[closest_date]
        # Calculate Market Cap
        market_cap = closest_row['Shares'] * filing_date_stock_price['Close'].iloc[0]
        market_cap = float(market_cap)
        market_caps.append(market_cap)

    return market_caps
