from ariadne import ObjectType, QueryType
from ariadne import graphql_sync, make_executable_schema
from ariadne.constants import PLAYGROUND_HTML

from datetime import datetime

from flaskr import app
from flask import request, jsonify

from models.errors import Error
from models.market.stocks import stock_query
from market.stocks.client import stocks_client

query = QueryType()
stock = ObjectType("Stock")

definition = """
    type Query {
        stock(ticker: String): Stock
    }

    type Stock {
        ticker: String!
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

@query.field("stock")
def resolve_stock(*_, ticker=None):
    stock = {}
    
    if ticker:
        stock['ticker'] = ticker
    
    return stock

@stock.field('financial')
def resolve_financial(obj, _):
    financial = {}
    try:
        query = stock_query(obj['ticker'], attr="eps,pe,marketcap,shares")
        response = stocks_client.attrs(query)
        if (response): financial = response
    except Exception as error:
        app.logger.error(error)
        raise error

    return financial

@stock.field("historical")
def resolve_historical(obj, _, begin: str, end: str):
    if not begin or not end:
        error = Error('Error in request input: please provide both begin and end dates.')
        app.logger.error(error)
        raise  error

    begin_date = None
    end_date = None
    try:
        begin_date = datetime.fromisoformat(begin)
    except Exception as error:
        app.logger.error("Error resolving 'begin_date'", error)
        raise Error('Error in request input: please provide begin date in proper iso format.')

    try:
        end_date = datetime.fromisoformat(end)
    except Exception as error:
        app.logger.error("Error resolving 'end_date'", error)
        raise Error('Error in request input: please provide end date in proper iso format.')

    historical = {}
    try:
        historical['begin'] = begin_date
        historical['end'] = end_date

        query = stock_query(obj['ticker'], begin_date, end_date)
        prices = stocks_client.fetch(query)
        if (prices): 
            historical['prices'] = prices

    except Exception as error:
        app.logger.error("Error resolving historical data", error)
        raise Error('Error occurred while resolving historical data')

    return historical

schema = make_executable_schema(definition, query, stock)

@app.route("/graphql", methods=["POST"])
def graphql_server():
    # GraphQL queries are always sent as POST
    data = request.get_json()

    # Note: Passing the request to the context is optional.
    # In Flask, the current request is always accessible as flask.request
    success, result = graphql_sync(
        schema,
        data,
        context_value=request,
        debug=app.debug
    )

    status_code = 200 if success else 400
    return jsonify(result), status_code

@app.route("/graphql", methods=["GET"])
def graphql_playground():
 
    # On GET request serve GraphQL Playground
    # You don't need to provide Playground if you don't want to
    # but keep on mind this will not prohibit clients from
    # exploring your API using desktop GraphQL Playground app.
    return PLAYGROUND_HTML, 200

if __name__ == "__main__":
    app.run(debug=True)