
from datetime import datetime
from models.market.stocks import stock_query
from market.stocks import stocks

query = stock_query('AAPL', datetime(2019, 1, 1), datetime(2020, 1, 1))
price_data = stocks.fetch(query)
print(price_data)