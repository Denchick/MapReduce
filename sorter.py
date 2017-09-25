#!/usr/bin/env python3
""" Внешняя сортировка """

import sys
import os
import argparse


def debug(s, flag):
    if flag:
        print(s)


class Map:
    def mapper(count, filename):
        """ Разделяет большой файл на несколько, 
        в каждом из которых count значений """
        print('Mapper is start...')
        with open(filename, 'r') as big:
            current_index = 0
            while True:
                with open('part_{}'.format(current_index), 'w') as f:
                    data = read_from_file(big, count)
                    if not data:
                        break
                    data = list(map(str, sorted(data)))
                    f.write('\n'.join(data))
                current_index += 1
        debug('Готово!', flag)

    def delete(prefix, countfiles):
        """ Удаляет временные файлы """
        for x in (prefix + str(i) for i in range(countfiles)):
            os.remove(x)
        debug('Временные файлы удалены.', flag)

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

class Reduce:
    def index_min(values):
        return min(enumerate(values), key=lambda x: x[1])[0]

    def read_from_file(file, count):
        data = []
        for i in range(count):
            try:
                temp = int(file.readline())
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

    def reducer(count, output_file, flag):
        """ Сливает много отсортированных файлов в один """
        debug('Reducer is start...', flag)
        files = get_opened_mapped_files("part_")
        with open(output_file, 'w') as output:
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
        debug('Трах-бах, готово!', flag)


def create_parser():
    """Parsing arguments"""
    parser = argparse.ArgumentParser(
        description="""Внешняя сортировка большого файла
        Вход: большой файл (не входящий в память).
        Выход: отсортированный файл.""".format())

    parser.add_argument(
        '-f', '--filename', type=open, help='"большой файл"')
    parser.add_argument(
        '-o', '--output', type=str, help='имя отсортированного файла')
    parser.add_argument(
        '-s', '--separator', type=str, default='\n',
        help='разделитель между значениями исходного файла')
    parser.add_argument(
        '-d', '--debug',
        action='store_true', help='debug mode', default=False)

    return parser.parse_args()


def main():
    parser = create_parser()
    args = parser.parse_args()
    mapper(args.count, args.filename, args.flag)
    reducer(args.count, args.output, args.flag)

if __name__ == "__main__":
    main()
