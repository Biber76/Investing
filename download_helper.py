import pandas as pd

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