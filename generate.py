#!/usr/bin/env python3

import random
import argparse
import logging


def random_generation(countOfNumbers, range_, filename, separator):
    """	Record numbers in range in filename with separator """
    logging.info('Generation is start.')
    count = 0
    with open(filename, 'w') as f:
        while (count < countOfNumbers):
            print(random.randint(range_[0], range_[1]),
                  file=f, sep=separator)
            count += 1
    logging.info('Generate.')


def parse_args():
    """Parsing arguments"""
    parser = argparse.ArgumentParser(
        usage='%(prog)s [OPTIONS]',
        description='Generating a "big file" of numbers'.format())

    parser.add_argument(
        '-o', '--output', type=str, default='generated.txt',
        metavar='FILENAME', help='name of output file')
    parser.add_argument(
        '-r', '--range', type=str, default='(-100, 100)',
        help='range generated values. Format: (leftBorder, rightBorder)')
    parser.add_argument(
        '-s', '--separator', type=str, default='\n',
        help='separator between values')
    parser.add_argument(
        'count', type=int, default=10,
        help='count values for generation')
    parser.add_argument(
        '-d', '--debug',
        action='store_true', help='debug mode')

    return parser.parse_args()


def main():
    args = parse_args()

    random_generation(
        args.count,
        tuple(map(int, args.range[1:-1].split(', '))),
        args.output,
        args.separator)


if __name__ == "__main__":
    main()
