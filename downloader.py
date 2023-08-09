from download_helper import Downloader, TickerUniverseUpdate
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from plotting_helper import PlotChartAsPDF
from processing_helper import CreatePlotFeatures
import tamb.mbindicator as mbi
import tamb.mbsignals as mbs
import tamb.mbplot as mbp # pypdf2 has to be changed to pypdf
from tqdm import tqdm
import yfinance as yf

# tickers from the evaluation.csv and update.csv are added to the universe.csv
# there is no check if those tickers work. That is done py the Downloader
ticker_universe_update = TickerUniverseUpdate()
ticker_universe_update.update_tickers()
df_ticker_universe, df_ticker_update, df_ticker_evaluation = ticker_universe_update.receive_ticker_dataframes()

# The Downloader downloads only one of the three df's. It starts with the df_ticker update
# as if we want to add a new ticker, we not necessarily want to download all other tickers as well.
# second, if the update.csv is empty, the evaluation.csv is used as we sometimes only want to calculate something
# with a few tickers and not all of them. If both files are empty, we download all tickers to update all data.
# If there is a download error, the universe.csv is being updated that those tickers are no longer in the universe.
downloader = Downloader(df_ticker_universe, df_ticker_update, df_ticker_evaluation)
downloader.download()
tickerlist = downloader.return_tickerlist()
print(tickerlist)

for i, ticker in enumerate(tickerlist):
    create_ticker = CreatePlotFeatures(tickerlist[i])
    processed_df = create_ticker.create_features()

    plotter = PlotChartAsPDF(tickerlist[i], processed_df, lookback=250)
    plotter.create_pdf()
