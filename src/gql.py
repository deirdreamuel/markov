from typing import List
from ariadne import ObjectType, QueryType
from ariadne import make_executable_schema

from datetime import datetime

from models.errors import Error
from models.market.stocks import StockQuery, StockDetails
from market.stocks import stocks
from market.exchange import exchange, stock_exchanges

from pandas import isna

# graphql query types
query = QueryType()
stock = ObjectType("Stock")
stock_market = ObjectType("StockMarket")

# graphql schema definition
definition = """
    type Query {
        stock(exchange: String, symbol: String): Stock
        stock_market(exchange: String): StockMarket
    }

    type StockMarket {
        exchange: String!
        industries: [String!]!
        symbols: [String!]!
        sectors: [String!]!
        stocks(industry: String, sector: String): [Stock]
    }

    type Stock {
        symbol: String!
        name: String
        country: String
        industry: String
        sector: String
        ipo: Int
        financial: FinancialData
        historical(begin: String, end: String): HistoricalData
    }

    type FinancialData {
        marketcap: Float
        eps: Float
        pe: Float
        shares: Float
    }

    type HistoricalData {
        begin: String!
        end: String!
        prices: [StockPrice]
    }

    type StockPrice {
        date: String!
        open: Float!
        close: Float!
        low: Float!
        high: Float!
        volume: Float!
    }
"""


@query.field("stock_market")
def resolve_stock_market(*_, exchange: str):
    if not exchange or not exchange.isalpha:
        raise Error(f"Error in request input: please enter valid stock market exchange parameter.")

    stock_market = {}
    try:
        exchange = exchange.upper().strip()
        stock_market['exchange'] = exchange
        stock_market['industries'] = sorted(stock_exchanges[exchange]['Industry'].dropna().unique())
        stock_market['sectors'] = sorted(stock_exchanges[exchange]['Sector'].dropna().unique())
        stock_market['symbols'] = sorted(stock_exchanges[exchange]['Symbol'].dropna().unique())

    except Exception:
        raise Error(f"Error in request input: unsupported stock exchange '{exchange}'")
        
    return stock_market

@stock_market.field("stocks")
def resolve_stocks(obj, _, industry: str = "", sector: str = ""):
    stocks = None
    try:
        exchange = obj['exchange']
        industry = industry.strip()
        sector = sector.strip()

        industry_query = stock_exchanges[exchange]["Industry"].str.contains(industry, False)
        sector_query = stock_exchanges[exchange]["Sector"].str.contains(sector, False)

        companies = []
        entries = stock_exchanges[exchange][industry_query & sector_query]
        for entry in entries.to_dict('records'):
            company = StockDetails()
            for key in entry.keys():
                if not isna(entry[key]):
                    setattr(company, key.lower(), entry[key])
            
            companies.append(company.object())

        stocks = companies
    except Exception:
        raise Error(f"Error in request input: unsupported stock exchange '{exchange}'")

    return stocks
    
@query.field("stock")
def resolve_stock(*_, symbol: str, exchange: str = 'NASDAQ'):
    if not exchange or not exchange.isalpha:
        raise Error(f"Error in request input: please enter valid stock market exchange parameter.")

    if not symbol:
        raise Error(f"Error in request input: please enter stock symbol parameter.")
    
    stock = None
    try:
        company = StockDetails()
        symbol = symbol.upper().strip()
        setattr(company, 'symbol', symbol)

        query_result = stock_exchanges[exchange].query(
            f'Symbol == "{symbol}"').to_dict('records')[0]
        for key in query_result.keys():
            if not isna(query_result[key]):
                setattr(company, key.lower(), query_result[key])

        stock = company.object()
        
    except IndexError:
        raise Error(f"Error in request input: cannot find stock '{symbol}' in '{exchange}' stock exchange")
    except Exception:
        raise Error(f"Error in request input: unsupported stock exchange '{exchange}'")
        
    return stock

@stock.field('financial')
def resolve_financial(obj, _):
    financial = {}
    try:
        query = StockQuery(obj['symbol'], attr="eps,pe,marketcap,shares")
        financial = stocks.attrs(query)

    except Exception as error:
        raise error

    return financial

@stock.field("historical")
def resolve_historical(obj, _, begin: str, end: str):
    if not begin or not end:
        raise Error('Error in request input: please provide both begin and end dates.')

    begin_date = None
    end_date = None
    try:
        begin_date = datetime.fromisoformat(begin)
    except Exception as error:
        raise Error('Error in request input: please provide begin date in proper iso format.')

    try:
        end_date = datetime.fromisoformat(end)
    except Exception as error:
        raise Error('Error in request input: please provide end date in proper iso format.')

    historical = {}
    try:
        historical['begin'] = begin_date
        historical['end'] = end_date

        query = StockQuery(obj['symbol'], begin_date, end_date)
        prices = stocks.fetch(query)
        if (prices): 
            historical['prices'] = prices

    except Exception as error:
        raise Error('Error occurred while resolving historical data')

    return historical

schema = make_executable_schema(definition, query, stock, stock_market)