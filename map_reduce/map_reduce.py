import os
import psutil
from . import extremum, piece, utils


class MapReduce:
    def __init__(self, separator, temp_directory, size_of_one_piece, source_filename=None, case_sensitive=True):
        """ Конcтруктор класса MapReduce.
        
        Args:
            separator(str): разделитель между значениями в сортируемом файле.
            temp_directory(str): папка для хранения временных файлов.
            size_of_one_piece(int): примерное место(нижняя граница) для хранения одного куска файла в памяти.
            source_filename(str): название файла для сортировки или None, если данные поступают с stdin.
            case_sensitive(bool): если сортируются строки, учитывается их регистр, иначе параметр не влияет на работу.
                
        Raises:
            TypeError: если разделитель не строка.
            """
        utils.check_file_path(source_filename)
        self.source_filename = source_filename
        if not isinstance(separator, str):
            raise TypeError("Разделитель между значениями должен быть строкой.")
        self.separator = separator
        self.pieces = []
        self.temp_directory = temp_directory
        self.case_sensitive = case_sensitive
        self.size_of_one_piece = size_of_one_piece

    @property
    def pieces_is_empty(self):
        """ Проверяет, остались ли еще хоть в одном кусочке элементы.
        
        Returns:
            True, если есть хоть один непрочитанный до конца кусочек, иначе False.
        """
        for p in self.pieces:
            if p is not None:
                return False
        return True

    def key_sort_piece(self, obj):
        """ Ключ для сортировки 
        
        Returns:
             comparable object.   
        """
        if utils.is_number(obj):
            try:
                return int(obj)
            except ValueError:
                return float(obj)
        if isinstance(obj, str):
            if self.case_sensitive:
                return obj
            return obj.lower()
        raise TypeError("Я (пока) не умею сравнивать объекты типа {0}!".format(type(obj)))

    def mapper(self, reverse=False, size_of_one_piece=None):
        """ Разделяет большой файл на несколько файлов, записывая их в папку temp_directory. 
        Если такой папки нет, то она будет создана.
        Внутри каждого кусочка значения разделяются переносом строки и сортируются в соответствии с параметрами.
        Размер одного кусочка не меньше, чем size_of_one_piece байт.
        
        Args:
            reverse (bool): сортировать ли значения внутри кусочка в обратном порядке.
            size_of_one_piece(int): примерное количество байт(нижняя граница), отводимое для одного куска файла.
            
        Raises:
            RuntimeError: если папка для временных файлов оказалась непуста. 
        """
        print('Mapper is start...')
        try:
            utils.check_directory_path(self.temp_directory)
        except FileNotFoundError:
            os.makedirs(self.temp_directory)

        if len(os.listdir(self.temp_directory)) > 0:
            raise RuntimeError("{0} папка не пуста!".format(self.temp_directory))
        with open(self.source_filename, 'r') as source_file:
            if size_of_one_piece is None:
                size_of_one_piece = psutil.virtual_memory().free // 10  # этот размер с лихвой должен влезать в память
            while True:
                piece_data = utils.get_next_data_piece(source_file, size_of_one_piece, self.separator)
                if len(piece_data) == 0:
                    break
                piece_data = '\n'.join(
                    sorted(piece_data.split(self.separator), reverse=reverse, key=self.key_sort_piece))
                self.pieces.append(
                    piece.Piece(len(self.pieces), piece_data, self.temp_directory))
        print('Done!')

    def reducer(self, output_filename, separator):
        """ Сливает много отсортированных файлов обратно в 1 файл. 
        Среди всех кусков смотрится верхний еще не добавленный в файл элемент, и из них выбирается экстремум - 
        наибольший или наименьший элемент, в зависимости от настройки алгоритма, а в соответствующем куске указатель
        на верхний элемент сдвигается на следующий после него элемент. Если кусок прочитан до конца, то он становится 
        None. Алгоритм заканчивает свою работу, когда все кусочки были дочитаны до конца, то есть стали None.

        Args:
            output_filename(str): имя файла, в который нужно собрать обратно большой файл.
            separator(str): разделитель между значениями в отсортированном файле.
        """
        print('Reducer is  start...')
        with open(output_filename, 'w') as output:
            while True:
                # Найдем экстремум.
                extr = None
                for piece in self.pieces:
                    if piece is None:
                        continue
                    element = piece.get_up_element(self.directory)
                    if extr is None or self.key_sort_piece(extr.data) < self.key_sort_piece(element):
                        extr = extremum.Extremum(element, piece)

                if extr is None or extr.data is None:
                    break # оказалось, что все куски пусты, алгоритм закончил работу.

                # экстремум найден, теперь его нужно удалить из соответствующего файла и положить в output.
                output.write(extr.data + separator)
                extr.piece_obj.move_data_pointer(len(extr.data) + len(separator))
                if extr.piece_obj.is_empty(self.directory):
                    self.pieces[extr.piece_obj.index] = None
        print('Done!')
