import numpy as np
import yfinance as yf
import pandas as pd


tickerlist_screener = pd.read_csv('./Data_Summary/Tickerlist_Screen.csv')
tickerlist_screener.columns = ['Ticker']
tickerlist = [i for i in tickerlist_screener['Ticker']]
# tickerlist =['BBBY']
missing_tickers = []
COUNT = 1

for ticker in tickerlist[:]:
    
    df = yf.download(ticker, period="max")
    if len(df) < 2:
        print(f'{COUNT}. missing ticker {ticker}')
        COUNT += 1
        missing_tickers.append(ticker)
        continue
    
    df['1d_chg'] = df['Close'].pct_change()
    df['1d_chg_log'] = np.log(df.Close) - np.log(df.Close.shift(1))
    df.to_csv(f"./Data/{ticker}.csv")
    print(f"./Data/{ticker}.csv", "created")

print(f'The tickers that caused an error are: {missing_tickers}')
print(f'The lenght of the DataFrame before correction is {len(tickerlist_screener)}')

for error_ticker in missing_tickers:
    tickerlist_screener.drop(tickerlist_screener[tickerlist_screener.Ticker == error_ticker].index, inplace=True)
print(f'The lenght of the DataFrame after correction is {len(tickerlist_screener)}')

tickerlist_screener.to_csv('./Data_Summary/Tickerlist_Screen.csv', index=False)
