#!/usr/bin/env python3

import argparse
import sys
from typing import Optional, List
from rich.console import Console
from rich.table import Table

from kaori.plugins.gacha.engine import Card
from kaori.plugins.gacha.engine.test import run_card_simulator, run_battle_simulator, cards
from kaori.plugins.gacha.engine.test.battle_simulator import BattleResult
from kaori.plugins.gacha.engine.test.utils import find_card

card_command = argparse.ArgumentParser(description='Simulate cards and their values.')
card_command.add_argument('--raw',
                          '-r',
                          action='store_true',
                          dest='raw',
                          default=False,
                          help='print output in raw markdown')

battle_command = argparse.ArgumentParser(description='Process some integers.')
battle_command.add_argument('card_A',
                            metavar='card_name',
                            type=str,
                            help='first card')
battle_command.add_argument('card_B',
                            metavar='card_name',
                            type=str,
                            help='second card')
battle_command.add_argument('--debug',
                            '-d',
                            dest='debug',
                            type=bool,
                            default=False,
                            help='verbose debugging statements')
battle_command.add_argument('--interactive',
                            '-i',
                            dest='interactive',
                            type=bool,
                            default=False,
                            help='run battle step by step in dramatic fashion')
battle_command.add_argument('--num-battle',
                            '-n',
                            dest='repeat',
                            type=int,
                            default=1,
                            help='repeat battle N times')

gen_command = argparse.ArgumentParser(description='create cards')
gen_command.add_argument('-R',
                         dest='rarity',
                         metavar='rarity',
                         type=str,
                         help='rarity: one of S, A, B, C, F')
gen_command.add_argument('--name',
                         metavar='card_name',
                         type=str,
                         help='card name')
gen_command.add_argument('natures',
                         metavar='natures',
                         nargs=2,
                         type=str,
                         help='Choose two natures from Stupid Baby Clown Horny Cursed Feral')

console = Console()

def main():
    command = sys.argv[1]

    if command == 'cards':
        args = card_command.parse_args(sys.argv[2:])
        return run_card_simulator(args.raw)

    if command == 'generate':
        args = gen_command.parse_args(sys.argv[2:])
        card = Card.generate(name=args.name,
                             rarity=args.rarity,
                             natures=args.natures)
        card.is_valid_card()
        console.print(card.to_rich_table())
        return

    if command == 'battle':
        args = battle_command.parse_args(sys.argv[2:])
        card_a = find_card(cards, args.card_A)
        card_b = find_card(cards, args.card_B)
        
        results: List[BattleResult] = []

        battle_table = Table(title=f"{card_a.title} VS. {card_b.title}", show_header=False)
        battle_table.add_column(card_a.title, justify="center")
        battle_table.add_column(card_b.title, justify="center")
        battle_table.add_row(card_a.to_rich_table(), card_b.to_rich_table())
        console.print(battle_table)
        
        for i in range(args.repeat):
            result = run_battle_simulator(card_a,
                                          card_b,
                                          debug=args.debug,
                                          interactive=args.interactive)
            if result:
                results.append(result)

        if len(results) > 0:
            aggregate = {}
            for result in results:
                if not result.winner.slug + '_wins' in aggregate:
                    aggregate[result.winner.slug + '_wins'] = 0
                aggregate[result.winner.slug + '_wins'] += 1

            print(aggregate)

        return

    raise RuntimeError('invalid command')


if __name__ == '__main__':
    main()
