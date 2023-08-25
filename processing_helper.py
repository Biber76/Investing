import numpy as np
import pandas as pd
import tamb.mbindicator as mbi
import tamb.mbsignals as mbs
import tamb.mbplot as mbp

class CreatePlotFeatures():
    
    def __init__(self, ticker) -> None:
        self.ticker = ticker
        
    def create_features(self):
        
        todays_signals = []
        failed = []
        
        try:
            df = pd.read_csv('./Data/{}.csv'.format(self.ticker), parse_dates=True, index_col='Date')
            
            df['ema20'] = df['Close'].ewm(span=20, adjust=False).mean()
            df['ema75'] = df['Close'].ewm(span=75, adjust=False).mean()
            df['ema144'] = df['Close'].ewm(span=144, adjust=False).mean()

            df['rising_ema20'] = (df['ema20'] > df['ema20'].shift(1)).astype(int)
            df['rising_ema75'] = (df['ema75'] > df['ema75'].shift(1)).astype(int)
            df['rising_Signal_ema'] = df.apply((lambda row: 2 if row.rising_ema75 == 1 and row.rising_ema20 == 1 \
                else 1 if row.rising_ema75 == 1 and row.rising_ema20 == 0 \
                else -1 if row.rising_ema75 == 0 and row.rising_ema20 == 1 \
                else -2), axis=1)
            df['rising_Signal_ema_TwoStage'] = mbi.TwoStageMovingAverageSignal(df)

            df['RSI'] = mbi.RSI(list(df.Close), 14)
            df['RSIdouble'] = mbi.RSIdouble(list(df.Close), 14)

            df['Stoch_D_slow'] = mbi.StochS(df, 5, 2, 3)
            df['Stoch_D_slow_LT'] = mbi.StochS(df, 22, 3, 5)

            df['SentimentIndicator_3'] = mbi.SentimentIndicator(df, 3)
            df['SentimentIndicator_7'] = mbi.SentimentIndicator(df, 7)
            df['SentimentIndicator_14'] = mbi.SentimentIndicator(df, 14)
            df['SentimentIndicator_20'] = mbi.SentimentIndicator(df, 20)
            df['SentimentIndicator_40'] = mbi.SentimentIndicator(df, 40)

            df['SentimentOverbought_bearish'] = mbs.SentimentOverboughBearish(df)
            df['SentimentOverboughtExhaustion'] = mbs.SentimentOverboughtExhaustions(df)
            if df['SentimentOverboughtExhaustion'][-1] == 1:
                todays_signals.append(self.ticker)

            df['IntSec_Low'] = mbs.IntersectionLow(df)
            df['IntSec_High'] = mbs.IntersectionHigh(df)

            df['td_sell_setup'] = mbs.tdSellSetup(df)
            if df['td_sell_setup'][-1] == 9:
                todays_signals.append(self.ticker)
            df['td_buy_setup'] = mbs.tdBuySetup(df)
            if df['td_buy_setup'][-1] == 9:
                todays_signals.append(self.ticker)

            df['td_sell_setup_inter'] = mbs.tdSellSetupInter(df)
            df['td_buy_setup_inter'] = mbs.tdBuySetupInter(df)

            df['td_sell_countdown'] = mbs.tdSellCountdown(df)
            if df['td_sell_countdown'][-1] == 13:
                todays_signals.append(self.ticker)
            df['td_buy_countdown'] = mbs.tdBuyCountdown(df)
            if df['td_buy_countdown'][-1] == 13:
                todays_signals.append(self.ticker)

            df['Chart_Low_Bars'] = mbs.ChartLowBars(df)
            if df['Chart_Low_Bars'][-1] == 1:
                todays_signals.append(self.ticker)
            df['Chart_Low_Deep_Bars'] = mbs.ChartLowDeepBars(df)
            if df['Chart_Low_Deep_Bars'][-1] == 1:
                todays_signals.append((self.ticker))
            df['Chart_Low_Bars_High_RSI'] = mbs.ChartLowBarsHighRSI(df)
            if df['Chart_Low_Bars_High_RSI'][-1] == 1:
                todays_signals.append(self.ticker)

            df['Color'] = mbp.ColoredBars(df)
            df['TrendColor'] = mbp.TrendColor(df)

            return df
        
        except:
            failed.append(self.ticker)
            print(f'{self.ticker} can not be processed')

        
    def return_ticker(self):
        return self.ticker
