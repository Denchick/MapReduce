#!/usr/bin/env python3

#mktemp
import math
import os
import argparse

GENERATED_FILE = 'generated.txt'


def index_min(values):
    return min(enumerate(values), key=lambda x: x[1])[0]


def debug(string):
    if True:
        print(string)


def read_from_file(f, count):
    data = []
    for i in range(count):
        try:
            temp = int(f.readline())
            data.append(temp)
        except ValueError:
            break
    return data


def read_first_elements_from_files(files):
    data = []
    for f in files:
        try:
            data.append(int(f.readline()))
        except ValueError:
            pass
    return data


def delete(prefix, countfiles):
    """ Удаляет временные файлы """
    for x in (prefix + str(i) for i in range(countfiles)):
        os.remove(x)
    debug('Temp files are deleted.')


def get_opened_mapped_files(prefix):
    """ Возвращает список открытых временных файлов """
    files = []
    current_index = 0
    while True:
        try:
            file_name = prefix + str(current_index)
            files.append(open(file_name, 'r'))
            current_index += 1
        except FileNotFoundError:
            return files


def close_mapped_files(files):
    for f in files:
        f.close()


def mapper(one_piece):
    """
    Разделяет большой файл на несколько, в каждом из которых one_piece значений
    """
    print('Mapper is start...')
    with open(GENERATED_FILE, 'r') as big:
        current_index = 0
        while True:
            with open('part_{}'.format(current_index), 'w') as f:
                data = read_from_file(big, one_piece)
                if not data:
                    break

                data = list(map(str, sorted(data)))
                f.write('\n'.join(data))
            current_index += 1
    debug('Done!')


def reducer(one_piece):
    debug('Reducer is start...')
    files = get_opened_mapped_files("part_")
    with open('output', 'w') as output:
        firsts = read_first_elements_from_files(files) # Список первых элементов из всех файлов
        while True:
            index = index_min(firsts) # найдем индекс минимального элемента
            if firsts[index] == math.inf:
                break
            output.write(str(firsts[index]) + '\n') # Запишем в output наименьший элемент
            temp = files[index].readline()
            if temp == '':
                firsts[index] = math.inf #тип больше, чем макс. возможное
            else:
                firsts[index] = int(temp)
    close_mapped_files(files)
    debug('Done!')


def parse_args():
    """Parsing arguments"""
    parser = argparse.ArgumentParser(
        usage='%(prog)s [OPTIONS]',
        description='External sorting a large file'.format())

    parser.add_argument(
        '-o', '--outputput', type=str, default='generated.txt',
        metavar='FILENAME', help='name of outputput file')
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
    one_piece = 10
    mapper(one_piece)
    reducer(one_piece)

if __name__ == "__main__":
    main()
