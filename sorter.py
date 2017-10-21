#!/usr/bin/env python3
""" Внешняя сортировка """

ERROR_EXCEPTION = 1
ERROR_WRONG_SETTINGS = 2
ERROR_PYTHON_VERSION = 3
ERROR_MODULES_MISSING = 4

import sys

if sys.version_info < (3, 0):
    print('Используйте Python версии 3.0 и выше', file=sys.stderr)
    sys.exit(ERROR_PYTHON_VERSION)

import argparse

try:
    from map_reduce import extremum, map_reduce, piece, utils
except Exception as e:
    print('Модули не найдены: "{}"'.format(e), file=sys.stderr)
    sys.exit(ERROR_MODULES_MISSING)

__version__ = '0.11'
__author__ = 'Volkov Denis'
__email__ = 'denchick1997@mail.ru'


def create_parser():
    """ Разбор аргументов командной строки """
    parser = argparse.ArgumentParser(
        description="""Внешняя сортировка большого файла, не помещающегося в память.
        Вход: файл, который нужно отсортировать.
        Выход: отсортированный файл.""")

    parser.add_argument(
        'filename', type=str, help='"большой файл"')
    parser.add_argument(
        '-o', '--output', type=str, help='имя отсортированного файла', default='output')
    parser.add_argument(
        '-t', '--temp', type=str, help='имя каталога для хранения временных файлов', default='temp')
    parser.add_argument(
        '-p', '--piece', type=int, help='примерное количество байт, отводимое на 1 временный файл', default=None)
    parser.add_argument(
        '-s', '--separator', type=str, default='\n',
        help='разделитель между значениями исходного файла')
    parser.add_argument(
        '-r', '--reverse',
        action='store_true', help='сортировка в обратном порядке', default=False)
    parser.add_argument(
        '-d', '--debug',
        action='store_true', help='debug mode', default=False)
    return parser.parse_args()


def main():
    args = create_parser()
    map_reduce_obj = map_reduce.MapReduce(args.filename, args.separator, args.temp, args.piece)
    map_reduce_obj.mapper(args.temp, args.reverse)
    map_reduce_obj.reducer(args.output, args.separator)

if __name__ == "__main__":
    main()
