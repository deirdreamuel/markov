from api.google.service import service
from market.stocks import client
from models.market.stocks import stock_price, stock_query

class google_finance(client):
    id: str

    def __init__(self, id) -> None:
        self.id = id
        super().__init__()

    def fetch(self, query: stock_query):
        data = None

        try:
            # cell input value
            sheets_input = '=GOOGLEFINANCE("{0}", "{1}", {2}, {3}, {4})'.format(
                query.ticker, query.attr, query.start_date.strftime("DATE(%Y,%m,%d)"),
                query.end_date.strftime("DATE(%Y,%m,%d)"), query.interval)

            input_value = {
                'values': [[sheets_input]]
            }

            # update spreadsheet then fetch all values
            service.update_spreadsheet(self.id, 'Sheet1!A1', input_value)
            result = service.get_spreadsheet(self.id, 'Sheet1!A2:F')
            stock_data = result['values']

            # format response to json stock data
            data = [stock_price]
            for i, _ in enumerate(stock_data):
                stock_entry = stock_price()

                for (j, field) in enumerate(stock_price.__dataclass_fields__):
                    setattr(stock_entry, field, stock_data[i][j])

                data.append(stock_entry)

        except Exception as error:
            print("Google finance error:", error)
        
        return data

finance = google_finance("1e3km5HHUvzEJx53kCkErvtldAr8_zrUgzXEvo757TYs")