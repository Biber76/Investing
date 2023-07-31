import numpy as np
import yfinance as yf
import pandas as pd


tickerlist_screener = pd.read_csv('./Data_Summary/Tickerlist_Screen.csv', header=None)
tickerlist_screener.columns = ['Ticker']
tickerlist = [i for i in tickerlist_screener['Ticker']]

for ticker in tickerlist[:3]:
    df = yf.download(ticker, period="max")
    df['1d_chg'] = df['Close'].pct_change()
    df['1d_chg_log'] = np.log(df.Close) - np.log(df.Close.shift(1))
    df.to_csv(f"./Data/{ticker}.csv")
    print(f"./Data/{ticker}.csv", "created")
