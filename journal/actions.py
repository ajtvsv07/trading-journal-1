import datetime
from typing import List, Optional

import click

from .journal import Journal

journal = Journal()


@click.command()
@click.option('--underlying', prompt='Underlying', type=str)
@click.option('--underlying_price', prompt='Underlying price', type=float)
@click.option('--iv_rank', prompt='IV rank', type=float)
@click.option('--strategy', prompt='Strategy name', type=str)
@click.option('--quantity', prompt='Quantity', type=int)
@click.option('--expiration',
              prompt='Expiration date',
              help='Format: 2021-17-09',
              type=str)
@click.option('--strikes',
              prompt='Strikes',
              help='Format: 70/80, 50/60/90/100',
              type=str)
@click.option('--premium', prompt='Premium', type=float)
@click.option('--margin', prompt='Margin', type=float)
@click.option('--timestamp', default=None, help='Format: 2021-08-16 17:30:50')
@click.option('--second_expiration', default=None, help='Format: 2021-17-09')
@click.option('--option_types', default=None, help='Format: P/C')
@click.option('--quantities', default=None, help='Format: -1/-1, +1/-1/-1/+1')
@click.option('--notes', default=None)
def open_position(underlying: str,
                  underlying_price: float,
                  iv_rank: float,
                  strategy: str,
                  quantity: int,
                  expiration: str,
                  strikes: List[float],
                  premium: float,
                  margin: float = None,
                  timestamp: Optional[str] = datetime.datetime.now(),
                  second_expiration: Optional[str] = None,
                  option_types: Optional[str] = None,
                  quantities: Optional[str] = None,
                  notes: Optional[str] = None):
    expiration = datetime.datetime.strptime(expiration, '%Y-%m-%d').date()
    strikes = strikes.split('/')
    strategy = strategy.upper()
    underlying = underlying.upper()

    assert len(underlying) <= 5

    if isinstance(timestamp, str):
        timestamp = datetime.datetime.strptime(timestamp,
                                               '%Y-%m-%d %H:%M:%S').date()

    if second_expiration is not None:
        second_expiration = datetime.datetime.strptime(second_expiration,
                                                       '%Y-%m-%d').date()

    if option_types is not None:
        option_types = option_types.split('/')

    if quantities is not None:
        quantities = quantities.split('/')

    journal.open_trade(
        **{
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
            'notes': notes
        })

    click.echo(
        click.style(f'Position on {underlying} has been added, thank you!',
                    fg='green'))


@click.command()
@click.option('--position_id', prompt='Position ID', type=int)
@click.option('--underlying_price', prompt='Underlying price', type=float)
@click.option('--iv_rank', prompt='IV rank', type=float)
@click.option('--premium', prompt='Premium', type=float)
@click.option('--timestamp', default=None, help='Format: 2021-08-16 17:30:50')
@click.option('--notes', default=None)
def close_position(
        position_id: int,
        underlying_price: float,
        iv_rank: float,
        premium: float,
        timestamp: Optional[datetime.datetime] = datetime.datetime.now(),
        notes: Optional[str] = None):
    if isinstance(timestamp, str):
        timestamp = datetime.datetime.strptime(timestamp,
                                               '%Y-%m-%d %H:%M:%S').date()

    journal.close_trade(
        **{
            'position_id': position_id,
            'underlying_price': underlying_price,
            'iv_rank': iv_rank,
            'premium': premium,
            'timestamp': timestamp,
            'notes': notes,
        })

    click.echo(
        click.style(f'Trade {position_id} has been closed, thank you!',
                    fg='green'))


@click.command()
@click.option('--position_id', prompt='Position ID', type=int)
@click.option('--underlying_price', prompt='Underlying price', type=float)
@click.option('--iv_rank', prompt='IV rank', type=float)
@click.option('--premium', prompt='Premium', type=float)
@click.option('--timestamp', default=None, help='Format: 2021-08-16 17:30:50')
@click.option('--notes', default=None)
def adjust_position(
        position_id: int,
        underlying_price: float,
        iv_rank: float,
        premium: float,
        strikes: str,
        timestamp: Optional[datetime.datetime] = datetime.datetime.now(),
        margin: Optional[float] = None,
        second_expiration: Optional[str] = None,
        option_types: Optional[str] = None,
        quantities: Optional[str] = None,
        notes: Optional[str] = None):
    strikes = strikes.split('/')

    if isinstance(timestamp, str):
        timestamp = datetime.datetime.strptime(timestamp,
                                               '%Y-%m-%d %H:%M:%S').date()

    if second_expiration is not None:
        second_expiration = datetime.datetime.strptime(second_expiration,
                                                       '%Y-%m-%d').date()

    if option_types is not None:
        option_types = option_types.split('/')

    if quantities is not None:
        quantities = quantities.split('/')

    journal.adjust_trade(
        **{
            'position_id': position_id,
            'underlying_price': underlying_price,
            'iv_rank': iv_rank,
            'premium': premium,
            'strikes': strikes,
            'timestamp': timestamp,
            'margin': margin,
            'second_expiration': second_expiration,
            'option_types': option_types,
            'quantities': quantities,
            'notes': notes,
        })

    click.echo(
        click.style(f'Position {position_id} has been adjusted, thank you!',
                    fg='green'))


@click.command()
@click.option('--symbol', prompt='Symbol', type=str)
@click.option('--direction', prompt='Direction', help='LONG/SHORT', type=str)
@click.option('--quantity', prompt='Quantity', type=int)
@click.option('--price', prompt='Price', type=float)
@click.option('--margin', prompt='Margin', type=float)
@click.option('--timestamp', default=None, help='Format: 2021-08-16 17:30:50')
@click.option('--notes', default=None)
def trade_underlying(
        symbol: str,
        direction: str,
        quantity: int,
        price: float,
        margin: float,
        timestamp: Optional[datetime.datetime] = datetime.datetime.now(),
        notes: Optional[str] = None):

    if isinstance(timestamp, str):
        timestamp = datetime.datetime.strptime(timestamp,
                                               '%Y-%m-%d %H:%M:%S').date()

    journal.equity_trade(
        **{
            'symbol': symbol,
            'direction': direction,
            'quantity': quantity,
            'price': price,
            'margin': margin,
            'timestamp': timestamp,
            'notes': notes,
        })

    click.echo(
        click.style(
            f'Trade on underlying: {symbol} has been added, thank you!',
            fg='green'))
