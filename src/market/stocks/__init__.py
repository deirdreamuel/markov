from api.google.finance import finance
from market.stocks.interface import IStockClient

stocks = IStockClient(finance)