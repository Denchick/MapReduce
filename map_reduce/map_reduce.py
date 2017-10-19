import os
import psutil
from . import extremum, piece, utils


class MapReduce:
    def __init__(self, source_filename, separator, temp_directory, size_of_one_piece, case_sensitive=True):
        utils.check_file_path(source_filename)
        self.source_filename = source_filename
        if not isinstance(separator, str):
            raise TypeError("Separator must be a string")
        self.separator = separator
        self.pieces = []
        self.directory = temp_directory
        self.case_sensitive = case_sensitive
        self.size_of_one_piece = size_of_one_piece

    def pieces_is_empty(self):
        for piece in self.pieces:
            if piece is not None:
                return False
        return True

    def key_sort_piece(self, obj):
        if utils.is_number(obj):
            try:
                return int(obj)
            except ValueError:
                return float(obj)
        if isinstance(obj, str):
            if self.case_sensitive:
                return obj
            return obj.lower()
        raise TypeError("I can't compare instances of {0} type!".format(type(obj)))

    def mapper(self, directory, reverse=False, size_of_one_piece=None):
        """ Разделяет большой файл на несколько """
        print('Mapper is start...')
        try:
            utils.check_directory_path(directory)
        except FileNotFoundError as e:
            os.makedirs(directory)
        if len(os.listdir(directory)) > 0:
            raise RuntimeError("{0} folder is not empty!".format(directory))
        with open(self.source_filename, 'r') as source_file:
            if size_of_one_piece is None:
                size_of_one_piece = psutil.virtual_memory().free // 100  # этот размер с лихвой должен влезать в память
            while True:
                piece_data = utils.get_next_data_piece(source_file, size_of_one_piece, self.separator)
                if len(piece_data) == 0:
                    break
                piece_data = self.separator.join(
                    sorted(piece_data.split(self.separator), reverse=reverse, key=self.key_sort_piece))
                self.pieces.append(piece.Piece(len(self.pieces), piece_data, directory))
        print('Done!')

    def reducer(self, output_filename, separator):
        """ Сливает много отсортированных файлов в один """
        print('Reducer is  start...')
        with open(output_filename, 'w') as output:
            while True:
                # Найдем экстремум
                extr = None
                for piece in self.pieces:
                    if piece is None:
                        continue

                    element = piece.get_up_element(self.directory, separator)
                    if extr is None or utils.comparator(
                            self.key_sort_piece(extr.data), self.key_sort_piece(element)) == 1:
                        extr = extremum.Extremum(element, piece)
                if extr is None or extr.data is None:
                    break
                # экстремум найден, теперь его нужно удалить из соответствующего файла и положить в output
                output.write(extr.data + separator)
                extr.piece_obj.move_data_pointer(len(extr.data) + len(separator))
                if extr.piece_obj.is_empty(self.directory):
                    self.pieces[extr.piece_obj.index] = None
        print('Done!')
