#!/usr/bin/env python3
""" Внешняя сортировка """

import sys
import os
import argparse
import tempfile
import psutil


class Extremum:
    def __init__(self, data, piece_obj):
        self.data = data
        self.piece_obj = piece_obj


class Piece:
    def __init__(self, index, data, directory):
        self.index = index
        self.data_pointer = 0  # каретка
        self.write_to_filename(data, directory)

    def write_to_filename(self, data, directory):
        """ Запись данных в directory/index """
        path = os.path.join(directory, self.index)
        with open(path, 'w') as f:
            f.write(data)

    def get_data(self, directory):
        """ Чтение данных из directory/index """
        path = os.path.join(directory, self.index)
        with open(path, 'r') as f:
            return f.read()

    def get_up_element(self, directory, separator):
        """  Читает данные из соответствующего файла  
        начиная с data_pointer пока не дойдет до separator"""
        path = os.path.join(directory, self.index)
        with open(path, 'r') as f:
            f.seek(self.data_pointer)
            result = ''
            while True:
                current = f.read(1)
                # Если separator из нескольких символов
                if current == '' or current == separator:
                    break
                result += separator
            return result

    def move_data_pointer(self, offset):  # kek, как будет смешение по-английски?
        """ Смешает data_pointer на смещение
        :type offset: сместить указатель на offset
        """
        assert isinstance(offset, int)
        self.data_pointer += offset

    def is_empty(self, directory):
        """ Проверяет, прочитан ли до конца файл """
        path = os.path.join(directory, self.index)
        with open(path, 'r') as f:
            f.seek(self.data_pointer)
            if f.read(1) == '':
                return True
            return False


class MapReduce:
    def __init__(self, source_filename, separator):
        self.source_filename = source_filename
        self.separator = separator
        self.pieces = []

    def get_next_data_piece(self, source_file, size_of_piece, separator):
        """ Возвращает следующий кусок данных из source_file """
        result = source_file.read(size_of_piece)
        if not result.endswith(separator):
            current = source_file.read(1)
            # что делать с separator?
            while current != '' and current != separator:
                result += current
                current = source_file.read(1)
        return result

    def comparator(self, value1, value2, *args, **kwargs):
        """ Должен сравнивать результат с нужными ключами """
        if self.isfloat(value1) and self.isfloat(value2):
            #числа, все ок
        if isinstance(value1, str) and isinstance(value2, str):
            #строки, все ок
        raise ValueError("What is it?")

    def mapper(self, source_filename, separator, directory):
        """ Разделяет большой файл на несколько"""
        print('Mapper is start...')
        with open(source_filename, 'r') as source_file:
            size_of_one_piece = psutil.virtual_memory().free / 1000  # этот размер с лихвой должен влезть в память
            while True:
                piece_data = self.get_next_data_piece(source_file, size_of_one_piece, separator)
                if len(piece_data) == 0:
                    break
                self.pieces.append(Piece(len(self.pieces), piece_data, directory))
        print('Готово!')

    def pieces_is_empty(self):
        for piece in self.pieces:
            if piece is not None:
                return False
        return True


    def isfloat(self, s):
        try:
            float(s)
            return True
        except ValueError:
            return False

    def reducer(self, output_filename, separator):
        """ Сливает много отсортированных файлов в один """
        print('Reducer is  start...')
        with open(output_filename, 'w') as output:
            while True:
                # Найдем экстремум
                extr = Extremum(self.pieces[0].get_up_element(separator), self.pieces[0])
                for piece in self.pieces:
                    if piece is None:
                        continue
                    element = piece.get_up_element(separator)
                    if self.comparator(extr.data, element):
                        extr = Extremum(element, piece)
                if extr.data is None:
                    break
                # экстремум найден, теперь его нужно удалить из соответствующего файла и положить в output
                output.write(extr.data + separator)
                extr.piece_obj.move_data_pointer(len(extr.data))
                if extr.piece_obj.is_empty():
                    self.pieces[extr.piece_obj.index] = None
        print('Трах-бах, готово!')


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
    #parser = create_parser()
    #args = parser.parse_args()
    #mapper(args.count, args.filename, args.flag)
    #reducer(args.count, args.output, args.flag)



if __name__ == "__main__":
    main()
