from market.stocks.client import StockClient
from models.market.stocks import StockQuery
from typing import List

class IStockClient:
    __client: StockClient

    def __init__(self, client) -> None:
        self.__client = client

    def fetch(self, query: StockQuery) -> List[object]:
        return self.__client.fetch(query)
    
    def attr(self, query: StockQuery) -> object:
        return self.__client.attr(query)

    def attrs(self, query: StockQuery) -> object:
        return self.__client.attrs(query)