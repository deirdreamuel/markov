## Installation

### Generate Google API key
generate your google service account and update ```src/api/google/credentials.json```. You can visit [Google API Page](https://cloud.google.com/docs/authentication/production) for an in-depth guide of obtaining service account credentials.

### Setup virtual environment
setup virtual environment with python3
``` bash
virtualenv env -p python3
source ./env/bin/activate

pip install -r requirements.txt
```

### Run GraphQL Server locally
make sure you have properly setup your environment
Run Flask server 

``` bash
python src/gql.py
```

then it should be running on ```localhost:5000/graphql```.

### Sample GraphQL query
here is a simple graphql query to obtain stock information using the api,

``` graphql
query {
  stock (symbol:"GOOG") {
    symbol,
    financial {
        marketcap,
        pe,
        eps,
        shares
    },
    historical (begin:"2011-10-02", end:"2021-10-24") {
      begin,
      end,
      prices {
      	date,
        open,
        close,
        high,
        low,
        volume
      }
    }
  }
}
```

