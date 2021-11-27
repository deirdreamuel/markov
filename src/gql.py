from ariadne import QueryType, graphql_sync, make_executable_schema
from ariadne import ObjectType
from ariadne.constants import PLAYGROUND_HTML

from flaskr import app
from flask import request, jsonify

from datetime import datetime
from models.market.stocks import stock_query
from market.stocks.client import stocks_client

query = QueryType()

@query.field("stock")
def resolve_stock(*_, ticker=None):
    if ticker:
        return {
            'ticker': ticker,
        }

stock = ObjectType("Stock")

@stock.field("historical")
def resolve_historical(obj, _, begin: str, end: str):
    if begin and end:
        begin_date = datetime.fromisoformat(begin)
        end_date = datetime.fromisoformat(end)

        query = stock_query(obj['ticker'], begin_date, end_date)
        prices = stocks_client.fetch(query)

        return {
            'begin': begin_date,
            'end': end_date,
            'prices': prices
        }

    return {}

definition = """
    type Query {
        stock(ticker: String): Stock
    }

    type Stock {
        ticker: String!
        historical(begin: String, end: String): StockData
    }

    type StockData {
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
        volume: Int!
    }
"""

schema = make_executable_schema(definition, query, stock)


@app.route("/graphql", methods=["GET"])
def graphql_playground():
    # On GET request serve GraphQL Playground
    # You don't need to provide Playground if you don't want to
    # but keep on mind this will not prohibit clients from
    # exploring your API using desktop GraphQL Playground app.
    return PLAYGROUND_HTML, 200


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


if __name__ == "__main__":
    app.run(debug=True)