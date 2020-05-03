#!/usr/bin/env python3

import argparse
import sys

from kaori.plugins.gacha.engine.test import run_card_simulator, run_battle_simulator

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


def main():
    command = sys.argv[1]

    if command == 'cards':
        return run_card_simulator()

    if command == 'battle':
        args = battle_command.parse_args(sys.argv[2:])
        return run_battle_simulator(args.card_A, args.card_B,
                                    debug=args.debug, interactive=args.interactive)

    raise RuntimeError('invalid command')


if __name__ == '__main__':
    main()
