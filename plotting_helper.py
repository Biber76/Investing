import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import tamb.mbplot as mbp

class PlotChartAsPDF():
    
    def __init__(self, ticker, df, lookback=150) -> None:
        self.ticker = ticker
        self.df = df
        self.lookback = lookback
    
    def create_pdf(self):
        try:
            mbp.mbPlot(self.ticker, self.df, self.lookback)
            print(f'{self.ticker} is plotted')
        except:
            print(f'{self.ticker} can not be plotted')