import sys
import os
import argparse
import tempfile
import psutil
from . import extremum, piece, utils


class MapReduce:
    def __init__(self, source_filename, separator):
        self.source_filename = source_filename
        self.separator = separator
        self.pieces = []

    def mapper(self, directory='temp', reverse=False):
        """ Разделяет большой файл на несколько
        :type directory: str
        :type reverse: bool
        """
        print('Mapper is start...')
        with open(self.source_filename, 'r') as source_file:
            size_of_one_piece = psutil.virtual_memory().free / 1000  # этот размер с лихвой должен влезть в память
            while True:
                piece_data = self.get_next_data_piece(source_file, size_of_one_piece, self.separator)
                piece_data.sort(reverse=reverse)
                if len(piece_data) == 0:
                    break
                self.pieces.append(piece.Piece(len(self.pieces), piece_data, directory))
        print('Готово!')

    def pieces_is_empty(self):
        for piece in self.pieces:
            if piece is not None:
                return False
        return True

    def reducer(self, output_filename, separator):
        """ Сливает много отсортированных файлов в один """
        print('Reducer is  start...')
        with open(output_filename, 'w') as output:
            while True:
                # Найдем экстремум
                extr = extremum.Extremum(self.pieces[0].get_up_element(separator), self.pieces[0])
                for piece in self.pieces:
                    if piece is None:
                        continue
                    element = piece.get_up_element(separator)
                    if utils.comparator(extr.data, element) == -1:
                        extr = extremum.Extremum(element, piece)
                if extr.data is None:
                    break
                # экстремум найден, теперь его нужно удалить из соответствующего файла и положить в output
                output.write(extr.data + separator)
                extr.piece_obj.move_data_pointer(len(extr.data))
                if extr.piece_obj.is_empty():
                    self.pieces[extr.piece_obj.index] = None
        print('Трах-бах, готово!')
