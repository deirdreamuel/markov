## Installation
brew tap mongodb/brew
brew install mongodb-community@5.0

mongod --config /usr/local/etc/mongod.conf --fork
mongosh

## Generate Google API key
generate your google service account and update src/api/google/credentials.json

## Setup virtual environment
setup virtual environment with python3
```
virtualenv env -p python3
source ./env/bin/activate

pip install -r requirements.txt
```