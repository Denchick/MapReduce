#!/usr/bin/env python3
"""Генератор случайных чисел"""

import re
import sys
import random
import argparse
import logging


__version__ = '1.0'
__author__ = 'Volkov Denis'
__email__ = 'denchick1997@mail.ru'


def parse_range(string):
    """ Парсит строку с диапазоном генерируемых значений """
    m = re.match(r'\((-?\d+),(-?\d+)\)$', string)
    if not m:
        raise ValueError('"{0}" не диапазон значений'.format(string))
    a, b = int(m.group(1)), int(m.group(2))
    return min(a, b), max(a, b)


def numbers_generator(count_numbers, range_, filename, separator):
    """	Генерация случайных чисел """
    if count_numbers < 0:
        raise ValueError("Нельзя сгенерировать {} значений".format(count_numbers))
    logging.info('Запуск генерации.')
    original = sys.stdout
    if filename is not None:
        sys.stdout = open(filename, 'w')
    for count in range(count_numbers):
        print(random.randint(range_[0], range_[1]), end=separator)
    sys.stdout = original
    logging.info('Сгенерировано {} значений в диапазоне {} в {}.'
                 .format(count_numbers, range_, 'stdout' if filename is None else filename))


def create_parser():
    description = """ Генератор случайных чисел. 
    По умолчанию генерирует 10 чисел из диапазона (-100, 100), включая границы, разделенные переносом строки. """
    parser = argparse.ArgumentParser(
        description=description)
    parser.add_argument(
        '-o', '--output', type=str, help='Имя выходного файла. По умолчанию выход направлен в stdout.')
    parser.add_argument(
        '-r', '--range', type=parse_range, default=(-100, 100),
        help="""Диапазон генерируемых чисел в формате (leftBorder, rightBorder). Границы включаются. 
        По умолчанию (-100,100).""")
    parser.add_argument(
        '-s', '--separator', type=str, default='\n',
        help='Разделитель между значениями. По умолчанию перевод строки - \\n.')
    parser.add_argument(
        '-c', '--count', type=int, default=10,
        help='Количество генерируемых значений. По умолчанию 10.')
    parser.add_argument(
        '-d', '--debug',
        action='store_true', help='Режим debug.', default=False)

    return parser.parse_args()


def main():
    log_format = '%(asctime)s [%(levelname)s <%(name)s>] %(message)s'
    args = create_parser()
    logging.basicConfig(filename="numbers_generator.log",
                        level=logging.DEBUG if args.debug else logging.ERROR,
                        format=log_format,
                        filemode='w')
    args = create_parser()
    numbers_generator(
        args.count,
        args.range,
        args.output,
        args.separator.encode().decode('unicode-escape'))


if __name__ == "__main__":
    main()
