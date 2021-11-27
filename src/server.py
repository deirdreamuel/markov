
from datetime import datetime
from models.market.stocks import stock_query
from market.stocks.client import stocks_client

query = stock_query('AAPL', datetime(2019, 1, 1), datetime(2020, 1, 1))
price_data = stocks_client.fetch(query)
print(price_data)