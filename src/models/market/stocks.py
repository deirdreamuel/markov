from dataclasses import dataclass
from typing import Optional

@dataclass
class stock_company: 
    symbol= Optional[str]
    name = Optional[str]
    industry = Optional[str]
    sector = Optional[str]
    ipo = Optional[int]
    country = Optional[str]

    def __init__(self) -> None:
        self.symbol= None
        self.name = None
        self.industry = None
        self.sector = None
        self.ipo = None
        self.country = None
        pass

    def object(self):
        return {
            "symbol": self.symbol,
            "name": self.name,
            "industry": self.industry,
            "sector": self.sector,
            "ipo": self.ipo,
            "country": self.country,
        }
        
@dataclass
class stock_info:
    eps: Optional[float]
    marketcap: Optional[float]
    pe: Optional[float]
    shares: Optional[float]

    def __init__(self, eps=0, marketcap=-1.0, pe=0, shares=-1) -> None:
        self.eps = eps
        self.marketcap = marketcap
        self.pe = pe
        self.shares = shares

    def object(self):
        return {
            "eps": self.eps,
            "marketcap": self.marketcap,
            "pe": self.pe,
            "shares": self.shares,
        }

@dataclass
class stock_price:
    date: str
    open: float
    high: float
    low: float
    close: float
    volume: float

    def __init__(self, date='', open=-1.0, 
        high=-1.0, low=-1.0, close=-1.0, volume=-1) -> None:
        self.date = date
        self.open = open
        self.high = high
        self.low = low
        self.close = close
        self.volume = volume
    
    def object(self):
        return {
            "date": self.date,
            "open": self.open,
            "high": self.high,
            "low": self.low,
            "close": self.close,
            "volume": self.volume
        }


from datetime import datetime, date

@dataclass
class stock_query:
    symbol: str
    attr: str
    start_date: datetime
    end_date: datetime
    interval: int

    def __init__(self, symbol, start=date.today(), end=date.today(), attr='all', interval=1) -> None:
        self.symbol = symbol
        self.start_date = start
        self.end_date = end
        self.attr = attr
        self.interval = interval