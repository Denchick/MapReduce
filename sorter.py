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

__version__ = '0.2'
__author__ = 'Volkov Denis'
__email__ = 'denchick1997@mail.ru'


def create_parser():
    """ Разбор аргументов командной строки """
    parser = argparse.ArgumentParser(
        description="""Внешняя сортировка файла, не помещающегося в оперативную память. Если не указывать файл, 
        то данные будут браться из sys.stdin.""")

    parser.add_argument(
        '-f', '--filename', type=str, help='Файл, который необходимо отсортировать. По умолчанию stdin.')
    parser.add_argument(
        '-o', '--output', type=str, help='Название выхода - отсортированного файла. По умолчанию stdout.')
    parser.add_argument(
        '-t', '--temp', type=str,
        help='Название каталога для хранения временных файлов.', default='4addf7826094555610bc0d0638e01295')
    parser.add_argument(
        '-p', '--piece', type=int, default=100,
        help='Примерное количество байт, которое можно использовать в оперативной памяти.')
    parser.add_argument(
        '-s', '--separator', type=str, default='\n',
        help='Разделитель между значениями в исходном и отсортированном файле.')
    parser.add_argument(
        '-r', '--reverse', action='store_true', default=False, help='Сортировка в обратном порядке')
    parser.add_argument(
        '-c', '--case_sensitive', action='store_true', default=False, help='Регистрозависимая сортировка строк.')
    parser.add_argument(
        '-d', '--debug', action='store_true', default=False, help="""Режим debug. Временные файлы не удаляются. Warning! 
        В этом режиме папку с временными файлами необходимо удалять самостоятельно во избежание падения утилиты.""" )
    return parser.parse_args()


def main():
    args = create_parser()
    map_reduce.MapReduce(
        args.filename,
        args.separator,
        args.temp,
        args.piece,
        args.case_sensitive)


if __name__ == "__main__":
    main()
