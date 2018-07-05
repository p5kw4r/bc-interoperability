# bcio

A project towards blockchain interoperability.

## Dependencies

This project is built with:

- [Python](https://www.python.org/)
- [PyPA](https://pip.pypa.io/en/stable/) tool for installing Python packages
- [Sqlite3](https://www.sqlite.org/index.html) as dbms
- [Web3.py](https://web3py.readthedocs.io/en/stable/) for Ethereum integration
- [mcrpc](https://github.com/coblo/mcrpc) for MultiChain integration
- [python-bitcoinrpc](https://github.com/jgarzik/python-bitcoinrpc) for Bitcoin integration

## Setup

### General dependencies

Install dependencies using your favourite package manager:

```
# pacman -S python python-pip sqlite
```

> This project uses `python 3.6.5` and `sqlite 3.24.0`.

### Python dependencies

#### With virtual environment

Create a virtual environment within the project (for `python >= 3.3`):

```
$ python -m venv venv
```

Activate virtual environment:

```
$ source venv/bin/activate
```

Install dependencies:

```
(venv) $ pip install web3 mcrpc python-bitcoinrpc
```

Deactivate virtual environment:

```
(venv) $ deactivate
```

#### Without virtual environment

Install dependencies:

```
$ pip install --user web3 mcrpc python-bitcoinrpc
```

### Database

Launch a python interpreter:

```
$ python
```

Run the database setup:

```
>>> import database
>>> database.setup()
```

Calling the `setup` function of the `database` module will:

1. create tables for `credentials` and `transactions`
2. seed the `credentials` table with credentials for Ethereum, MultiChain and Bitcoin
3. seed the `transactions` table with input transactions for MultiChain and Bitcoin
