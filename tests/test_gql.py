import json
from flaskr import app

class TestGraphQL:
    def test_stock_info (self):
        query = '''query {
            stock (symbol:"GOOG") {
                symbol,
                name,
                sector,
                industry
            }
        }'''

        with app.test_client() as client:
            print('test_stock_info: testing basic stock info retrieval using graphql.')
            response = client.post('/graphql', json={'query': str(query)})
            assert response.status_code == 200

            obj = json.loads(response.data)['data']['stock']
            assert obj['symbol'] == 'GOOG'
            assert obj['name']
            assert obj['sector']
            assert obj['industry']