import datetime
import os
from typing import List, Optional

import numpy as np
import pandas as pd
import sqlalchemy
from dotenv import load_dotenv
from sqlalchemy import Column, ForeignKey, Table
from sqlalchemy.dialects.mysql import (DATE, DATETIME, ENUM, FLOAT, INTEGER,
                                       JSON, SMALLINT, TEXT, VARCHAR)


class Journal:
    def __init__(self):
        self.create_tables()

    @property
    def dotenv_file_path(self):
        # path = os.path.join(os.path.pardir, '.env')
        # path = os.path.join(os.path.dirname(__file__), '.env')
        path = os.path.join(os.path.abspath('.'), '.env')
        return path

    def create_tables(self):
        load_dotenv(self.dotenv_file_path)
        DATABASE_URL = os.environ.get('DATABASE_URL')
        assert DATABASE_URL, 'Please set env variable ( DATABASE_URL ) correctly.'
        self.engine = sqlalchemy.create_engine(DATABASE_URL)
        metadata = sqlalchemy.MetaData(self.engine)

        self.positions = Table(
            'positions',
            metadata,
            Column('id', INTEGER(), primary_key=True, autoincrement=True),
            Column('timestamp', DATETIME()),
            Column('underlying', VARCHAR(5)),

            # Snapshot on opening time
            Column('underlying_price', FLOAT(2)),
            Column('iv_rank', FLOAT(2)),

            # Position details
            Column('strategy', VARCHAR(30)),
            Column('quantity', INTEGER()),
            Column('expiration', DATE()),
            Column('strikes', JSON()),
            Column('premium', FLOAT(2)),
            Column('margin', FLOAT(2)),

            # Mostly null, but might be needed
            Column('second_expiration', DATE()),
            Column('option_types', JSON()),
            Column('quantities', JSON()),

            # Notes
            Column('notes', TEXT()),
        )

        self.trades = Table(
            'trades',
            metadata,
            Column('trade_id', INTEGER(), primary_key=True,
                   autoincrement=True),
            Column('position_id', ForeignKey('positions.id')),
            Column('timestamp', DATETIME()),

            # Snapshot on closing time
            Column('underlying_price', FLOAT(2)),
            Column('iv_rank', FLOAT(2)),

            # Closing price
            Column('premium', FLOAT(2)),

            # Notes
            Column('notes', TEXT()),
        )

        self.adjustments = Table(
            'adjustments',
            metadata,
            Column('adjustment_id',
                   INTEGER(),
                   primary_key=True,
                   autoincrement=True),
            Column('position_id', ForeignKey('positions.id')),
            Column('timestamp', DATETIME()),

            # Market Snapshot
            Column('underlying_price', FLOAT(2)),
            Column('iv_rank', FLOAT(2)),

            # Possible changes
            Column('option_types', JSON()),
            Column('quantities', JSON()),
            Column('strikes', JSON()),
            Column('expiration', DATE()),
            Column('second_expiration', DATE()),
            Column('margin', FLOAT(2)),

            # Additional credits/debits
            Column('premium', FLOAT(2)),

            # Notes
            Column('notes', TEXT()))

        self.equities = Table(
            'equities',
            metadata,
            Column('timestamp', DATETIME()),
            Column('symbol', VARCHAR(5)),
            Column('direction', ENUM('LONG', 'SHORT')),
            Column('quantity', SMALLINT()),
            Column('price', FLOAT(2)),
            Column('margin', FLOAT(2)),
            Column('notes', TEXT()),
        )

        metadata.create_all()

    # Write operations

    def open_trade(
        self,
        underlying: str,
        underlying_price: float,
        iv_rank: float,
        strategy: str,
        quantity: int,
        expiration: datetime.date,
        strikes: List[float],
        premium: float,
        margin: Optional[float] = None,
        timestamp: Optional[datetime.datetime] = datetime.datetime.now(),
        second_expiration: Optional[datetime.date] = None,
        option_types: Optional[List[str]] = None,
        quantities: Optional[List[int]] = None,
        notes: Optional[str] = None,
    ):
        sql = self.positions.insert({
            'underlying': underlying,
            'underlying_price': underlying_price,
            'iv_rank': iv_rank,
            'strategy': strategy,
            'quantity': quantity,
            'expiration': expiration,
            'strikes': strikes,
            'premium': premium,
            'margin': margin,
            'timestamp': timestamp,
            'second_expiration': second_expiration,
            'option_types': option_types,
            'quantities': quantities,
            'notes': notes,
        })

        with self.engine.connect() as conn:
            conn.execute(sql)

    def close_trade(
        self,
        position_id: int,
        underlying_price: float,
        iv_rank: float,
        premium: float,
        timestamp: Optional[datetime.datetime] = datetime.datetime.now(),
        notes: Optional[str] = None,
    ):
        sql = self.trades.insert({
            'position_id': position_id,
            'underlying_price': underlying_price,
            'iv_rank': iv_rank,
            'premium': premium,
            'timestamp': timestamp,
            'notes': notes,
        })

        with self.engine.connect() as conn:
            conn.execute(sql)

    def adjust_trade(
            self,
            position_id: int,
            underlying_price: float,
            iv_rank: float,
            premium: float,
            timestamp: Optional[datetime.datetime] = datetime.datetime.now(),
            option_types: Optional[List[str]] = None,
            quantities: Optional[List[int]] = None,
            strikes: Optional[List[float]] = None,
            expiration: Optional[datetime.date] = None,
            second_expiration: Optional[datetime.date] = None,
            margin: Optional[float] = None,
            notes: Optional[str] = None):
        assert any[option_types is not None, quantities is not None,
                   strikes is not None, expiration is not None,
                   second_expiration is not None]

        sql = self.adjustments.insert({
            'position_id': position_id,
            'underlying_price': underlying_price,
            'iv_rank': iv_rank,
            'premium': premium,
            'timestamp': timestamp,
            'option_types': option_types,
            'quantities': quantities,
            'strikes': strikes,
            'expiration': expiration,
            'second_expiration': second_expiration,
            'margin': margin,
            'notes': notes,
        })

        with self.engine.connect() as conn:
            conn.execute(sql)

    def equity_trade(
            self,
            symbol: str,
            direction: str,
            quantity: int,
            price: float,
            margin: float,
            timestamp: Optional[datetime.datetime] = datetime.datetime.now(),
            notes: Optional[str] = None):
        sql = self.equities.insert({
            'timestamp': timestamp,
            'symbol': symbol,
            'direction': direction,
            'quantity': quantity,
            'price': price,
            'margin': margin,
            'notes': notes,
        })

        with self.engine.connect() as conn:
            conn.execute(sql)

    # Read operations

    def get_positions(self):
        sql = '''
        SELECT *
            FROM positions
            WHERE id NOT IN (
                SELECT position_id
                FROM trades
            )
        '''

        positions = pd.read_sql(
            sql, self.engine.connect()).set_index('id').replace({
                'null': np.nan,
                None: np.nan
            })
        return positions

    def get_trades(self):
        sql = '''
        SELECT
            t.trade_id,
            p.strategy,
            p.quantity,
            p.expiration,
            p.strikes,
            p.timestamp AS entry_time,
            t.timestamp AS exit_time,
            p.underlying_price AS entry_price,
            t.underlying_price AS exit_price,
            p.iv_rank AS entry_ivr,
            t.iv_rank AS exit_ivr,
            p.premium AS entry_premium,
            t.premium AS exit_premium,
            p.margin,
            p.second_expiration,
            p.option_types,
            p.quantities,
            p.notes AS entry_notes,
            t.notes AS exit_notes
        FROM trades t
        INNER JOIN positions p
        WHERE
            t.position_id = p.id
        '''
        trades = pd.read_sql(
            sql, self.engine.connect()).set_index('trade_id').replace({
                'null':
                np.nan,
                None:
                np.nan
            })
        return trades

    # TODO: Number of adjustments for a trade
