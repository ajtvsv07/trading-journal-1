import click
from . import actions
from .journal import Journal


@click.command()
@click.option(
    '--action',
    prompt=click.style(
        '\n\nHi! Welcome to the trading journal.\n\nWhat would you like to do?\n\nOPEN (O) | CLOSE (C) | ADJUST (A) | TRADE UNDERLYING (U)',
        fg='green'),
    type=str)
def cli(action):
    journal = Journal()
    action = action.upper()
    positions = journal.get_positions()[['underlying', 'strategy']]
    positions.columns = [c.title() for c in positions.columns]
    positions.index.name = 'ID'

    if action in ['OPEN', 'O']:
        actions.open_position()

    elif action in ['CLOSE', 'C']:
        click.echo()
        actions.close_position()

    elif action in ['ADJUST', 'A']:
        click.echo(positions)
        actions.adjust_position()

    elif action in ['TRADE UNDERLYING', 'U']:
        actions.trade_underlying()

    else:
        raise ValueError('Selected wrong action.')
