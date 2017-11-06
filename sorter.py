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
import logging

try:
    from map_reduce import extremum, map_reduce, piece, utils
except Exception as e:
    print('Модули не найдены: "{}"'.format(e), file=sys.stderr)
    sys.exit(ERROR_MODULES_MISSING)

__version__ = '1.0'
__author__ = 'Volkov Denis'
__email__ = 'denchick1997@mail.ru'

LOGGER_NAME = 'sorter'
LOGGER = logging.getLogger(LOGGER_NAME)


def create_parser():
    """ Разбор аргументов командной строки """
    parser = argparse.ArgumentParser(
        description="""Внешняя сортировка файла, не помещающегося
        в оперативную память. Если не указывать файл, то данные
        будут браться из sys.stdin.""")
    parser.add_argument(
        '-f', '--filename', type=str,
        help="""Файл, который необходимо отсортировать.
        По умолчанию данные берутся из stdin.""")
    parser.add_argument(
        '-o', '--output', type=str,
        help="""Название выхода - отсортированного файла.
        По умолчанию данные направлены в stdout.""")
    parser.add_argument(
        '-t', '--temp', type=str,
        help="""Каталог для хранения временных файлов.
        По умолчанию создается временный каталог из модуля tempfile""")
    parser.add_argument(
        '-p', '--piece', type=int,
        help="""Примерное количество байт, которое можно
        использовать в оперативной памяти.""")
    parser.add_argument(
        '-s', '--separator', type=str, default='\n',
        help="""Разделитель между значениями в исходном и отсортированном
        файле. По умолчанию перевод строки.""")
    parser.add_argument(
        '-i', '--ignore-case', action='store_true', default=False,
        help="Игнорирование регистра символов")
    parser.add_argument(
        '-n', '--numeric-sort', action='store_true', default=False,
        help="Сравнивать значения как числа")
    parser.add_argument(
        '-r', '--reverse', action='store_true', default=False,
        help='Сортировка в обратном порядке')
    parser.add_argument(
        '-d', '--debug', action='store_true', default=False,
        help="""Режим debug. Временные файлы не удаляются. Warning!
        В этом режиме папку с временными файлами необходимо удалять
        самостоятельно во избежание падения утилиты.""")
    parser.add_argument(
        '--version', action='store_true', default=False,
        help="Печатает версию утилиты и выходит.")

    return parser.parse_args()


def main():
    args = create_parser()

    if args.version:
        print(__version__)
        sys.exit()

    log = logging.StreamHandler(sys.stderr)
    log.setFormatter(logging.Formatter(
        '%(asctime)s [%(levelname)s <%(name)s>] %(message)s'))

    for module_ in (sys.modules[__name__], map_reduce):
        logger = logging.getLogger(module_.LOGGER_NAME)
        logger.setLevel(logging.DEBUG if args.debug else logging.ERROR)
        logger.addHandler(log)

    map_reduce.MapReduce(
        input_filename=args.filename,
        output_filename=args.output,
        separator=args.separator,
        temp_directory=args.temp,
        size_of_one_piece=args.piece,
        ignore_case=args.ignore_case,
        numeric_sort=args.numeric_sort,
        reverse=args.reverse,
        debug=args.debug)


if __name__ == "__main__":
    main()
