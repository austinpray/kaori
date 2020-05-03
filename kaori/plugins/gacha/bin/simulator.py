#!/usr/bin/env python3

import argparse
import sys
from typing import Optional, List

from kaori.plugins.gacha.engine.test import run_card_simulator, run_battle_simulator
from kaori.plugins.gacha.engine.test.battle_simulator import BattleResult

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


def main():
    command = sys.argv[1]

    if command == 'cards':
        args = card_command.parse_args(sys.argv[2:])
        return run_card_simulator(args.raw)

    if command == 'battle':
        args = battle_command.parse_args(sys.argv[2:])
        results: List[BattleResult] = []
        for i in range(args.repeat):
            result = run_battle_simulator(args.card_A,
                                          args.card_B,
                                          print_header=(i == 0),
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
