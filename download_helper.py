from datetime import datetime
import numpy as np
import os
import pandas as pd
import time
from tqdm import tqdm
import yfinance as yf

def get_csv_file_change_date(file):
    try:
        change_timestamp = os.path.getmtime(f'./Data/{file}.csv')
        change_date = time.strftime('%Y-%m-%d', time.localtime(change_timestamp))
        return change_date
    except FileNotFoundError:
        return "File not found"
    except Exception as e:
        return f"An error occurred: {e}"
        

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
        
        tickerlist = [i for i in self.df['Ticker']] + ['^GSPC'] # Always download S&P as it is used for rel. strenght

        missing_tickers = []
        COUNT = 1

        for ticker in tqdm(tickerlist[:10]):
            
            if get_csv_file_change_date(ticker) == datetime.today().strftime('%Y-%m-%d'):
                print(f'The CSV file for the ticker {ticker} already exists and is up to date. No download necessary.')
                continue
            
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
        
    def return_tickerlist(self):
        tickerlist = [i for i in self.df['Ticker']] + ['^GSPC'] # Always download S&P as it is used for rel. strenght
        return tickerlist


class TickerUniverseUpdate():
    
    def __init__(self) -> None:
        
        self.df_A = pd.read_csv('./Data_Summary/Ticker_Universe.csv')
        self.df_B = pd.read_csv('./Data_Summary/Ticker_Update.csv')
        self.df_C = pd.read_csv('./Data_Summary/Ticker_Evaluation.csv')

    def update_tickers(self):
        # if there are new tickers, we first add them to the existing universe
        if len(self.df_B) > 0:
            df_D = pd.concat([self.df_A, self.df_B])
            self.df_A = df_D.drop_duplicates()
            self.df_A.to_csv('./Data_Summary/Ticker_Universe.csv', index=False)
            del df_D
            print('Ticker universe is being updated with Ticker_Update.csv!')

        # if there are tickers to evaluate, we add them to the existing universe
        if len(self.df_C) > 0:
            df_D = pd.concat([self.df_A, self.df_C])
            self.df_A = df_D.drop_duplicates()
            self.df_A.to_csv('./Data_Summary/Ticker_Universe.csv', index=False)
            del df_D
            print('Ticker universe is being updated with Ticker_Evaluation.csv!')
    
    def receive_ticker_dataframes(self):
        return self.df_A, self.df_B, self.df_C
    
