
from datetime import datetime
from models.market.stocks import stock_query
from market.stocks.client import google_client

query = stock_query('AAPL', datetime(2019, 1, 1), datetime(2020, 1, 1))
stocks_client = google_client
print(stocks_client.query(query))