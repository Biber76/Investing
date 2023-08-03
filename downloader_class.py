from download_helper import TickerUniverseUpdate
import numpy as np
import pandas as pd
from tqdm import tqdm
import yfinance as yf

ticker_universe_update = TickerUniverseUpdate()
ticker_universe_update.update_tickers()
df_ticker_universe, df_ticker_update, df_ticker_evaluation = ticker_universe_update.receive_ticker_dataframes()

print(f'ticker universe lenght {len(df_ticker_universe)}')

class Downloader():
    
    def __init__(self, df_ticker_universe, df_ticker_update, df_ticker_evaluation) -> None:
        self.df_ticker_universe = df_ticker_universe
        self.df_ticker_update = df_ticker_update
        self.df_ticker_evaluation = df_ticker_evaluation
        # select the dataframe to download the tickers
        # self.df is being created in the method below
        self.choose_dataframe()
    
    def choose_dataframe(self):
        if len(self.df_ticker_update) > 0:
            self.df = self.df_ticker_update
            return self.df
        if len(self.df_ticker_evaluation) > 0:
            self.df = self.df_ticker_evaluation
            return self.df
        self.df = self.df_ticker_universe
        return self.df
                        
    def download(self):
        
        tickerlist = [i for i in self.df['Ticker']]

        missing_tickers = []
        COUNT = 1

        for ticker in tqdm(tickerlist[:10]):
            
            df = yf.download(ticker, period="max")
            if len(df) < 2:
                print(f'{COUNT}. missing ticker {ticker}')
                COUNT += 1
                missing_tickers.append(ticker)
                continue
            
            df['1d_chg'] = df['Close'].pct_change()
            df['1d_chg_log'] = np.log(df.Close) - np.log(df.Close.shift(1))
            df.to_csv(f"./Data/{ticker}.csv")

        print(f'The tickers that caused an error are: {missing_tickers}')
        print(f'The lenght of the DataFrame before correction is {len(self.df_ticker_universe)}')

        for error_ticker in missing_tickers:
            self.df_ticker_universe.drop(self.df_ticker_universe[self.df_ticker_universe.Ticker == error_ticker].index, inplace=True)
        print(f'The lenght of the DataFrame after correction is {len(self.df_ticker_universe)}')

        self.df_ticker_universe.to_csv('./Data_Summary/Ticker_Universe.csv', index=False)

downloader = Downloader(df_ticker_universe, df_ticker_update, df_ticker_evaluation)
downloader.download()