from dataclasses import dataclass

@dataclass
class stock_price:
    date: str
    open: int
    high: int
    low: int
    close: int
    volume: int

    def __init__(self, date='', open='', 
        high=-1, low=-1, close=-1, volume=-1) -> None:
        self.date = date
        self.open = open
        self.high = high
        self.low = low
        self.close = close
        self.volume = volume


from datetime import datetime

@dataclass
class stock_query:
    ticker: str
    attr: str
    start_date: datetime
    end_date: datetime
    interval: int

    def __init__(self, ticker, start, end, attr='all', interval=1) -> None:
        self.ticker = ticker
        self.start_date = start
        self.end_date = end
        self.attr = attr
        self.interval = interval