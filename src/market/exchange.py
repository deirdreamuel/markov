import os
import pandas as pd
from pandas.core.frame import DataFrame

class Exchange:
    nyse: DataFrame
    nasdaq: DataFrame

    def __init__(self) -> None:
        self.nyse = pd.read_csv(os.path.dirname(__file__) + '/stocks/nyse.csv')
        self.nasdaq = pd.read_csv(os.path.dirname(__file__) + '/stocks/nasdaq.csv')

exchange = Exchange()

stock_exchanges = {
    'NYSE': exchange.nyse,
    'NASDAQ': exchange.nasdaq
}