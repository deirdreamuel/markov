from typing import List
from models.market.stocks import stock_query, stock_price

class client:
    def fetch(query: stock_query):
        raise 'stocks client fetch function template'

class stock_market:
    __client: client

    def __init__(self, client) -> None:
        self.__client = client

    def query(self, query: stock_query) -> List[stock_price]:
        return self.__client.fetch(query)