#!/usr/bin/env python3
"""Генератор случайных чисел"""


import re
import sys
import random
import argparse

def debug(s, flag):
    if flag:
        print(s)

def parse_range(string):
    m = re.match(r'\((-?\d+),(-?\d+)\)$', string)
    if not m:
        raise ValueError('"{0}" не диапазон значений'.format(string))
    a, b = int(m.group(1)), int(m.group(2))
    return (min(a, b), max(a, b))

def numbers_generator(count_numbers, range_, filename, separator, flag):
    """	Генерация случайных чисел """
    if count_numbers < 0:
        raise ValueError("Нельзя сгенерировать {} значений".format(count_numbers))
    debug('Запуск генерации.', flag)
    original = sys.stdout
    if filename is not None:
        sys.stdout = open(filename, 'w')
    for count in range(count_numbers):
        print(random.randint(range_[0], range_[1]), end=separator)
    stdout = original
    debug(r'Сгенерировано {} значений в диапазоне {} в {}.'
        .format(count_numbers, range_, filename), flag)



def create_parser():
    parser = argparse.ArgumentParser(
        description='Генерация большого файла случайных чисел'.format())

    parser.add_argument(
        '-o', '--output', type=str, help='имя выходного файла')
    parser.add_argument(
        '-r', '--range', type=parse_range, default=(-100, 100),
        help='диапазон генерируемых значений. Пример: (-100,100)')
    parser.add_argument(
        '-s', '--separator', type=str, default='\n',
        help='разделитель значений')
    parser.add_argument(
        '-c', '--count', type=int, default=10,
        help='количество генерируемых значений')
    parser.add_argument(
        '-d', '--debug',
        action='store_true', help='debug mode', default=False)

    return parser.parse_args()


def main():
    args = create_parser()
    numbers_generator(
        args.count,
        args.range,
        args.output,
        args.separator,
        args.debug)


if __name__ == "__main__":
    main()
