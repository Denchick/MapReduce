#!/usr/bin/env python3
"""Генератор случайных строк"""

import re
import sys
import random
import argparse
import string
import logging

__version__ = '1.0'
__author__ = 'Volkov Denis'
__email__ = 'denchick1997@mail.ru'


def parse_range(string_range):
    """ Парсит строку с диапапазоном генерируемых значений """
    m = re.match(r'\((-?\d+),(-?\d+)\)$', string_range)
    if not m:
        raise ValueError('"{0}" не диапазон длин строк'.format(string_range))
    a, b = int(m.group(1)), int(m.group(2))
    if a <= 0 or b <= 0:
        raise ValueError('Длина строки не может иметь не положительную длину: {}'
                         .format(min(a, b)))
    return min(a, b), max(a, b)


def get_random_string(chars, size=(1, 10), ):
    """ Генератор случайных символов из списка chars диапазона size """
    return ''.join(random.choice(chars) for _ in range(
        random.randint(size[0], size[1])))


def get_alphabet(has_digits, has_upper, has_lower, has_special):
    """ Формирует алфавит для генерации строк """
    chars = ''
    if has_digits:
        chars += string.digits
    if has_lower:
        chars += string.ascii_lowercase
    if has_upper:
        chars += string.ascii_uppercase
    if has_special:
        chars += string.punctuation
    if not has_digits and not has_lower and not has_upper and not has_special:
        chars = string.ascii_letters + string.digits + string.punctuation  # = digits + upper + lower + special
        logging.info('Строки будут состоять из цифр, строчных и прописных букв, специальных символов.')
    return chars


def random_strings_generator(has_digits, has_upper, has_lower, has_special,
                             count, size, separator, filename):
    """ Генератор случайных строк """
    chars = get_alphabet(has_digits, has_upper, has_lower, has_special)

    logging.info('Запуск генерации.')
    original = sys.stdout
    if filename is not None:
        sys.stdout = open(filename, 'w')
    for i in range(count):
        print(get_random_string(chars, size), end=separator)
    sys.stdout = original
    logging.info('Сгенерировано {} строк длинами {} в файл {}.'
                 .format(count, size, 'stdout' if filename is None else filename))


def create_parser():
    description = """Генератор случайных строк. 
    По умолчанию генерирует 10 строк, состоящих из цифр, прописных и заглавных букв английского алфавита,
    разделенных переносом строки."""
    parser = argparse.ArgumentParser(
        description=description)
    parser.add_argument(
        '-di', '--digits',
        action='store_true', help='В алфавите генерации есть цифры.', default=False)
    parser.add_argument(
        '-up', '--uppercase',
        action='store_true', help='В алфавите генерации есть прописные буквы.', default=False)
    parser.add_argument(
        '-lo', '--lowercase',
        action='store_true', help='В алфавите генерации есть строчные буквы.', default=False)
    parser.add_argument(
        '-sp', '--special',
        action='store_true', help='В алфавите генерации есть специальные символы из string.punctuation.', default=False)
    parser.add_argument(
        '-c', '--count', type=int, default=10,
        help='Количество генерируемых строк.')
    parser.add_argument(
        '-r', '--size_range', type=parse_range, default=(6, 18),
        help='Диапазон длин генерируемых строк в формате (leftBorder, rightBorder). Границы включаются. Пример: (6,18)')
    parser.add_argument(
        '-s', '--separator', type=str, default='\n',
        help='Разделитель между строками. По умолчанию это перевод строки.')
    parser.add_argument(
        '-o', '--output', type=str, help='Имя выходного файла. По умолчанию выход направлен в stdout.')
    parser.add_argument(
        '-d', '--debug',
        action='store_true', help='Режим debug.', default=False)

    return parser.parse_args()


def main():
    log_format = '%(asctime)s [%(levelname)s <%(name)s>] %(message)s'
    args = create_parser()
    logging.basicConfig(filename="string_generator.log",
                        level=logging.DEBUG if args.debug else logging.ERROR,
                        format=log_format,
                        filemode='w')
    random_strings_generator(
        args.digits,
        args.uppercase,
        args.lowercase,
        args.special,
        args.count,
        args.size_range,
        args.separator.encode().decode('unicode-escape'),
        args.output)


if __name__ == "__main__":
    main()
