from dataclasses import dataclass

@dataclass
class StockMarket:
    exchange: str
    industries: list
    symbols: list
    sectors: list
