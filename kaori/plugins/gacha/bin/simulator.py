#!/usr/bin/env python3

import argparse
import sys
from rich.console import Console

from kaori.plugins.gacha.engine import Card
from kaori.plugins.gacha.engine.test import run_card_simulator, run_battle_simulator2, run_cli_battle_simulator

card_command = argparse.ArgumentParser(description='Simulate cards and their values.')
card_command.add_argument('--raw',
                          '-r',
                          action='store_true',
                          dest='raw',
                          default=False,
                          help='print output in raw markdown')

battle_command = argparse.ArgumentParser(description='battle two cards')
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
                            action='store_true',
                            dest='debug',
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
battle_command.add_argument('--format',
                            '-f',
                            type=str,
                            default='cli',
                            help='can be one of cli, web, web_raw')

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

        if args.format.startswith('web'):
            run_battle_simulator2(card_a_name=args.card_A,
                                  card_b_name=args.card_B,
                                  repeat=args.repeat,
                                  out_format=args.format)
            return

        if args.format.startswith('cli'):
            run_cli_battle_simulator(card_a_name=args.card_A,
                                     card_b_name=args.card_B,
                                     console=console,
                                     repeat=args.repeat,
                                     out_format=args.format)
            return

    raise RuntimeError('invalid command')


if __name__ == '__main__':
    main()
