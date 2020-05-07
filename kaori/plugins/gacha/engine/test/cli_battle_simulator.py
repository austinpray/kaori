import urllib.parse
from typing import List
from rich.console import Console
from rich.progress import track
from rich.table import Table

import ujson

from . import cards as card_pool
from .utils import find_card
from .. import Card
from ..core.battle import Battle


def run_cli_battle_simulator(card_a_name: str,
                             card_b_name: str,
                             console: Console,
                             repeat: int = 1,
                             out_format: str = None,
                             debug: bool = False,
                             interactive: bool = False) -> List[Battle]:
    results: List[Battle] = []
    card_a: Card = find_card(card_pool, card_a_name)
    card_b: Card = find_card(card_pool, card_b_name)

    print_battle_table(card_a, card_b, console)

    for i in track(range(repeat), description="battling..."):

        if not card_a.id:
            card_a.id = 1
        if not card_b.id:
            card_b.id = card_a.id + 1

        results.append(Battle(card_a=card_a, card_b=card_b).run())

    # print_results(card_a, card_b, results, console)

    return results


def print_battle_table(card_a: Card, card_b: Card, console: Console):
    card_a_style = "bold royal_blue1"
    card_b_style = "bold yellow1"
    battle_table = Table(title=f"[{card_a_style}]{card_a.title}[/] [bold]VS.[/] [{card_b_style}]{card_b.title}[/]",
                         show_header=False)
    battle_table.add_column(card_a.title, justify="center")
    battle_table.add_column(card_b.title, justify="center")
    battle_table.add_row(card_a.to_rich_table(card_a_style), card_b.to_rich_table(card_b_style))

    console.print(battle_table)

# TODO: make this work...this throws the following:
#  card_a_wins = [r for r in results if r.winner.title == card_b.title]
#  AttributeError: 'NoneType' object has no attribute 'title'
def print_results(card_a: Card, card_b: Card, results: List[Battle], console: Console):
    card_a_wins = [r for r in results if r.winner.title == card_a.title]
    console.print(f"card_a wins: {len(card_a_wins)}")
    card_b_wins = [r for r in results if r.winner.title == card_b.title]
    console.print(f"card_b wins: {len(card_b_wins)}")