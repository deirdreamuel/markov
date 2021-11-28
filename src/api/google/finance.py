import json
from api.google.service import service
from market.stocks import client
from models.market.stocks import stock_info, stock_price, stock_query

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
            data = []
            for i, _ in enumerate(stock_data):
                stock_entry = stock_price()

                for (j, field) in enumerate(stock_price.__dataclass_fields__):
                    setattr(stock_entry, field, stock_data[i][j])

                data.append(stock_entry.object())

        except Exception as error:
            print("Google finance error fetch:", error)
            raise error
        
        return data

    def attr(self, query: stock_query):
        data = ''

        try:
            sheets_input = '=GOOGLEFINANCE("{0}", "{1}")'.format(query.ticker, query.attr)
            input_value = {
                'values': [[sheets_input]]
            }

            # update spreadsheet then fetch all values
            service.update_spreadsheet(self.id, 'Sheet1!A1', input_value)
            result = service.get_spreadsheet(self.id, 'Sheet1!A1:A1')

            data = result['values'][0][0]

        except Exception as error:
            print("Google finance error attr:", error)
            raise error

        return data

    def attrs(self, query: stock_query):
        data = ''

        try:
            attributes = query.attr.split(',')

            if (len(attributes) < 1):
                raise 'Error, please use multiple attributes in stock query'

            inputs = []
            read_range = 'Sheet1!A1:{0}1'.format(chr(ord('A') + len(attributes) - 1))

            for i in attributes:
                input = '=GOOGLEFINANCE("{0}", "{1}")'.format(query.ticker, i)
                inputs.append(input)

            input_value = {
                'values': [inputs]
            }

            # update spreadsheet then fetch all values
            service.update_spreadsheet(self.id, 'Sheet1!A1', input_value)
            result = service.get_spreadsheet(self.id, read_range)
            service.clear_spreadsheet(self.id, read_range)

            data = stock_info()
            for (i, attr) in enumerate(attributes):
                setattr(data, attr, result['values'][0][i])

        except Exception as error:
            print("Google finance error attrs:", error)
            raise error

        return data.object()

finance = google_finance("1e3km5HHUvzEJx53kCkErvtldAr8_zrUgzXEvo757TYs")