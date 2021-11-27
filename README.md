## Installation
brew tap mongodb/brew
brew install mongodb-community@5.0

mongod --config /usr/local/etc/mongod.conf --fork
mongosh

## Generate Google API key
generate your google service account and update ```src/api/google/credentials.json```. You can visit [Google API Page](https://cloud.google.com/docs/authentication/production) for an in-depth guide of obtaining service account credentials.

## Setup virtual environment
setup virtual environment with python3
```
virtualenv env -p python3
source ./env/bin/activate

pip install -r requirements.txt
```

## Run GraphQL Server locally
make sure you have properly setup your environment
Run Flask server 

```
python src/gql.py
```

then it should be running on ```localhost:5000/graphql```.

### Sample GraphQL query
here is a simple graphql query to obtain stock information using the api,

```
query {
  stock (ticker:"GOOG") {
    ticker,
    historical (begin:"2020-11-11", end:"2021-11-11") {
      begin,
      end,
      prices {
      	date,
        open,
        close,
        volume
      }
    }
  }
}
```

