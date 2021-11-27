from dataclasses import dataclass

@dataclass
class stock_price:
    date: str
    open: float
    high: float
    low: float
    close: float
    volume: int

    def __init__(self, date='', open=-1.0, 
        high=-1.0, low=-1.0, close=-1.0, volume=-1) -> None:
        self.date = date
        self.open = open
        self.high = high
        self.low = low
        self.close = close
        self.volume = volume
    
    def json(self):
        return {
            "date": self.date,
            "open": self.open,
            "high": self.high,
            "low": self.low,
            "close": self.close,
            "volume": self.volume
        }


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