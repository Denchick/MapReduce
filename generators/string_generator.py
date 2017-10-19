#!/usr/bin/env python3
"""Генератор случайных строк"""

import re
import sys
import random
import argparse
import string


def debug(s, flag):
    if flag:
        print(s)


def parse_range(string):
    m = re.match(r'\((-?\d+),(-?\d+)\)$', string)
    if not m:
        raise ValueError('"{0}" не диапазон длин строк'.format(string))
    a, b = int(m.group(1)), int(m.group(2))
    if a <= 0 or b <= 0:
        raise ValueError('Длина строки не может иметь не положительную длину: {}'
                         .format(min(a, b)))
    return min(a, b), max(a, b)


def get_random_string(chars, size=(1, 10), ):
    return ''.join(random.choice(chars) for _ in range(
        random.randint(size[0], size[1])))


def get_alphabet(has_digits, has_upper, has_lower, has_special, flag):
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
        debug('Строки будут состоять из цифр, строчных и прописных букв, специальных символов', flag)
    return chars


def random_strings_generator(has_digits, has_upper, has_lower, has_special,
                             count, size, separator, filename, flag):
    """ Генератор случайных строк """
    chars = get_alphabet(has_digits, has_upper, has_lower, has_special, flag)

    debug('Запуск генерации.', flag)
    original = sys.stdout
    if filename is not None:
        sys.stdout = open(filename, 'w')
    for i in range(count):
        print(get_random_string(chars, size), end=separator)
    stdout = original
    debug('Сгенерировано {} строк длинами {} в файл {}.'
          .format(count, size, filename), flag)


def create_parser():
    parser = argparse.ArgumentParser(
        description='Генератор случайных строк'.format())
    parser.add_argument(
        '-di', '--digits',
        action='store_true', help='цифры', default=False)
    parser.add_argument(
        '-up', '--uppercase',
        action='store_true', help='прописные буквы', default=False)
    parser.add_argument(
        '-lo', '--lowercase',
        action='store_true', help='строчные буквы', default=False)
    parser.add_argument(
        '-sp', '--special',
        action='store_true', help='специальные символы', default=False)
    parser.add_argument(
        '-c', '--count', type=int, default=10,
        help='количество генерируемых строк')
    parser.add_argument(
        '-r', '--size_range', type=parse_range, default=(6, 18),
        help='диапазон длин генерируемых строк. Пример: (6,18)')
    parser.add_argument(
        '-s', '--separator', type=str, default='\n',
        help='разделитель между значениями')
    parser.add_argument(
        '-o', '--output', type=str, help='имя выходного файла')
    parser.add_argument(
        '-d', '--debug',
        action='store_true', help='debug mode', default=False)

    return parser.parse_args()


def main():
    args = create_parser()
    random_strings_generator(
        args.digits,
        args.uppercase,
        args.lowercase,
        args.special,
        args.count,
        args.size_range,
        args.separator,
        args.output,
        args.debug)


if __name__ == "__main__":
    main()
