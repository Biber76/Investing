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

        if len(self.df_C) > 0:
            df_D = pd.concat([self.df_A, self.df_C])
            self.df_A = df_D.drop_duplicates()
            self.df_A.to_csv('./Data_Summary/Ticker_Universe.csv', index=False)
            del df_D
            print('Ticker universe is being updated with Ticker_Evaluation.csv!')
    
    def receive_ticker_dataframes(self):
        return self.df_A, self.df_B, self.df_C

ticker_universe_update = TickerUniverseUpdate()
ticker_universe_update.update_tickers()
df_ticker_universe, df_ticker_update, df_ticker_evaluation = ticker_universe_update.receive_ticker_dataframes()

print(df_ticker_evaluation.head())
print(df_ticker_universe.head())
print(df_ticker_update.head())

# df_A = pd.read_csv('./Data_Summary/Ticker_Universe.csv')
# df_B = pd.read_csv('./Data_Summary/Ticker_Update.csv')
# df_C = pd.read_csv('./Data_Summary/Ticker_Evaluation.csv')

# # if there are new tickers, we first add them to the existing universe
# if len(df_B) > 0:
#     df_D = pd.concat([df_A, df_B])
#     df_A = df_D.drop_duplicates()
#     df_A.to_csv('./Data_Summary/Ticker_Universe.csv', index=False)
#     del df_D
#     print('Ticker universe is being updated with Ticker_Update.csv!')

# if len(df_C) > 0:
#     df_D = pd.concat([df_A, df_C])
#     df_A = df_D.drop_duplicates()
#     df_A.to_csv('./Data_Summary/Ticker_Universe.csv', index=False)
#     del df_D
#     print('Ticker universe is being updated with Ticker_Evaluation.csv!')


# df_D = pd.concat([df_A, df_B])


# df_D.drop_duplicates(inplace=True)
