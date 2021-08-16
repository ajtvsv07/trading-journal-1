## Options Trading Journal

A trading journal built for options traders from options traders, with the emphasis on premium selling, tastytrade-style.

The goal is to track and organize information about the account's returns and the individual trades so that we can extract valuable insights from this information later on.

The lifetime of each options trade is made up of possible 4 stages:

1. Opening the position
2. Adjusting the position
3. Closing the position
4. Trading the underlying

For each position, we would like to track this information:

```
Current timestamp
Underlying
Current price
IV rank
Strategy name
Quantity
Expiration date
Strikes
Premium received/paid
Margin requirements
Notes
```

The database contains 4 tables, each one representing a different part of the trading process and linked with appropriate foreign keys.

The tables are:

- `positions`
- `trades`
- `adjustments`
- `equity_trades`

<b>Built using Python, MySQL, SQLAlchemy, click, pandas</b>

<b>NOTE</b>
This package is still a work in progress.

## Features

- MySQL database connection
- Functions for communicating with the database in a Pythonic way (opening, closing, adjusting positions and trading the underlying)
- Functions for reading data from the database into easy-to-work-with pandas DataFrame objects.
- Relational tables designed for:
  - New positions
  - Closed trades
  - Trade adjustments
  - Trades in the underlying
- Command-line interface

## Installation

<b>Clone the repo</b>

`git clone https://github.com/oriesh/trading-journal.git`

<b>Install with pip</b>

`cd path/to/package`
`pip install .`

<b>Setting environment variables</b>
Create a `.env` file inside the root and insert the database URL:

`DATABASE_URL="mysql+mysqlconnector://[user]:[password]@[host]/[dbname]"`

or export this environment variable:

`export DATABASE_URL="mysql+mysqlconnector://[user]:[password]@[host]/[dbname]"`

## Usage

To input data, initiate the CLI:

```python
python app.py
```

After that you'll be prompted for data collection.

Data analysis is done using the 2 jupyter notebooks in the `analytics` folder, one is used to analyze the trades in the trading journal (`trade_analytics.ipynb`), the other is used to analyze changes in the account balance (returns, `account_analytics.ipynb`).

Check them out.

## Contributions

You are more than welcomed to contribute to this package!

- Bulk insertion
  - Bulk insertion of positions, past trades, adjustments and equity trades.
- Front end
  - Right now the journal uses a CLI, it'd be nice to built a friendly UI for it.
  - The front end shall be built with ReactJS and SASS
- RESTful API
  - The future front end would need a way to communicate with our back end MySQL database.
  - The backend RESTful API shall be built with Flask.
  - Requests:
    ###### GET
    - `get_positions`
    - `get_trades`
    - `get_adjustments`
    - `get_equity_trades`
    - `get_trade_analytics`
    ###### POST
    - `open_position`
    - `close_position`
    - `adjust_position`
    - `trade_underlying`
    ###### PUT
    - `update_account_balance` - Send a CSV containing a series of account values and the corresponding dates, this will be used for the account analytics.
- Testing
  - Since I built this tool for myself and for other apps of mine to interract with, there's not enough QA done on it, for example: type checking, input value checking, etc.
  - Pytest is the preferred testing framework.
- Docs
  - Building documentation with Sphinx would be nice.
- Anything you think you can improve!
