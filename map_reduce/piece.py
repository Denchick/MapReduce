import os
from . import utils


class Piece:
    def __init__(self, index, data, directory):
        """ Конструктор кусочка - одного фрагмента большого файла.
        
        Args:
            index(int): порядковый номер части, на которую разбит исходный файл.
            data(str): данные, которые следует записать в кусок.
            directory(str): папка для хранения временных файлов - кусков. 
        """
        if not isinstance(index, int):
            raise TypeError("Index куска должен быть целым числом")
        utils.check_directory_path(directory)

        self.index = index
        self.data_pointer = 0  # каретка
        if os.path.exists(self.get_path(directory)):
            raise RuntimeWarning('Файл с индексом {0} уже существует'.format(self.index))
        self.write_to_filename(data, directory)

    def write_to_filename(self, data, directory):
        """ Запись данных в кусок. При этом, если в файле уже что-то было, то содержимое перезаписывается. 

        Args:
            data(str): данные, которые следует записать в файл. 
            directory(str): папка, в которой хранятся временные файлы - куски.
            
        Raises:
            TypeError: если data не строка.
        """
        utils.check_directory_path(directory)
        if not isinstance(data, str):
            raise TypeError("data должна быть строкой, а не {0}".format(type(data)))
        path = self.get_path(directory)
        with open(path, 'w') as f:
            f.write(data)

    def get_data(self, directory):
        """ Чтение данных из куска с 0 байта и до коцна файла. Указатель на верхний элемент не сдвигается.
 
        Args:
            directory(str): папка, в которой хранятся временные файлы - куски.       
        """
        path = self.get_path(directory)
        utils.check_file_path(path)
        with open(path, 'r') as f:
            return f.read()

    def get_up_element(self, directory):
        """ Получает верхний элемент куска.
        Читает строку в файле, начиная с указателя на верхний элемент. При этом, указатель не смещается. 

        Args:
            directory(str): папка, в которой хранятся временные файлы - куски.
        """
        utils.check_directory_path(directory)
        path = self.get_path(directory)
        with open(path, 'r') as f:
            f.seek(self.data_pointer)
            return f.readline()

    def move_data_pointer(self, offset):
        """ Смещает указатель на верхний элемент куска на offset байт

        Args:
            offset (int): смещение указателя(в байтах) 
        
        Raises:
            TypeError: если смещение не целое число.
            RuntimeError: если после смещения указатель на верхний элемент становится отрицательным.
        """
        if not isinstance(offset, int):
            raise TypeError("Смещение должно быть целым числом, но оказалось {0}.".format(type(offset)))
        if self.data_pointer + offset < 0:
            raise RuntimeError(
                "Невозможно сдвинуться на {0} байт, т.к. указатель на верхний элемент будет < 0".format(offset))
        self.data_pointer += offset

    def is_empty(self, directory):
        """ Проверяет, прочитан ли до конца кусок. 

        Args:
            directory(str): папка, в которой хранятся временные файлы - куски.
        """
        path = self.get_path(directory)
        with open(path, 'r') as f:
            f.seek(self.data_pointer)
            if f.read(1) == '':
                return True
            return False

    def get_path(self, directory):
        """ Формирует относительный путь до куска в виде: 'directory/index' в зависимости от ОС.

        Args:
            directory(str): папка, в которой хранятся временные файлы - куски.

        Returns:
            Относительный путь до соответствующего куска.
        """
        return os.path.join(directory, str(self.index))
