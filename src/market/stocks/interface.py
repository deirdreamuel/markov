from market.stocks.client import client
from models.market.stocks import stock_info, stock_query, stock_price
from typing import List

class interface:
    __client: client

    def __init__(self, client) -> None:
        self.__client = client

    def fetch(self, query: stock_query) -> List[object]:
        return self.__client.fetch(query)
    
    def attr(self, query: stock_query) -> object:
        return self.__client.attr(query)

    def attrs(self, query: stock_query) -> object:
        return self.__client.attrs(query)