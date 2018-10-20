# GraphShop
This is the server implementation of the GraphShop application.
It is also acting as the server environment for the recommendations
Data Mining project by Austin Graham.

## Running the server

Create virtual environment and acitvate:
```
python3 -m venv graphshop
source graphshop/bin/actvate
```

## Development and running unit tests:

Run the following for development mode:
```
python3 setup.py develop
```

Run unit tests:
```
nose2 -v --with-coverage --coverage-report term-missing
```
