import os
from . import utils


class Piece:
    def __init__(self, index, data, directory):
        if not isinstance(index, int):
            raise TypeError("Index of piece must be an int")
        if not isinstance(data, str):
            raise TypeError("Data must be a string")
        utils.check_directory_path(directory)

        self.index = index
        self.data_pointer = 0  # каретка
        if os.path.exists(self.get_path(directory)):
            raise RuntimeWarning('File with {0} index is exists'.format(self.index))
        self.write_to_filename(data, directory)

    def write_to_filename(self, data, directory):
        """ Запись данных в directory/index """
        utils.check_directory_path(directory)

        path = self.get_path(directory)
        with open(path, 'w') as f:
            f.write(data)

    def get_data(self, directory):
        """ Чтение всех данных из directory/index """
        path = self.get_path(directory)
        utils.check_file_path(path)
        with open(path, 'r') as f:
            return f.read()

    def get_up_element(self, directory, separator):
        """  Читает данные из соответствующего файла  
        начиная с data_pointer, пока не дойдет до separator """
        utils.check_directory_path(directory)
        if not isinstance(separator, str):
            raise TypeError("Separator must be a string")
        if separator == '':
            raise RuntimeError('Separator cannot be an empty string')

        path = self.get_path(directory)
        with open(path, 'r') as f:
            f.seek(self.data_pointer)
            result = ''
            while True:
                current = f.read(1)
                if len(result) == 0 and current == separator:
                    continue
                if current == '' or current == separator and len(result) > 0:
                    break
                result += current
            return result

    def move_data_pointer(self, offset):
        """ Смещает data_pointer на offset """
        if not isinstance(offset, int):
            raise TypeError("Offset must be an int")
        if self.data_pointer + offset < 0:
            raise RuntimeError("data_pointer must be greater than zero.")
        self.data_pointer += offset

    def is_empty(self, directory):
        """ Проверяет, прочитан ли до конца файл """
        path = self.get_path(directory)
        with open(path, 'r') as f:
            f.seek(self.data_pointer)
            if f.read(1) == '':
                return True
            return False

    def get_path(self, directory):
        return os.path.join(directory, str(self.index))
