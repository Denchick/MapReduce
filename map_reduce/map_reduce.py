import os
import shutil
import logging
import psutil
import sys

from . import extremum, piece, utils

LOGGER_NAME = 'map_reduce.map_reduce'
LOGGER = logging.getLogger(LOGGER_NAME)


class MapReduce:
    def __init__(self, input_filename='input.txt',
                 output_filename='output.txt',
                 separator=' ',
                 temp_directory='temp',
                 size_of_one_piece=100,
                 case_sensitive=True,
                 reverse=False,
                 debug=False):
        """ Конcтруктор класса MapReduce.
        
        Args:
            separator(str): разделитель между значениями в сортируемом файле.
            temp_directory(str): папка для хранения временных файлов.
            size_of_one_piece(int): примерное место(нижняя граница) для хранения одного куска файла в памяти.
            input_filename(str): название файла для сортировки или None, если данные поступают с stdin.
            case_sensitive(bool): если сортируются строки, учитывается их регистр, иначе параметр не влияет на работу.
            """
        LOGGER.info("Initialization of meta data.")
        self.input_filename = input_filename
        self.output_filename = output_filename
        self.separator = separator
        self.temp_directory = temp_directory
        self.size_of_one_piece = size_of_one_piece
        self.case_sensitive = case_sensitive
        self.reverse = reverse
        self.debug = debug
        self.pieces = []

        LOGGER.info("OK. Let's start to sorting.")
        self.run_sorting()

    def run_sorting(self):
        self.mapper()
        self.reducer()
        self.clean_up(self.debug)

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

    def mapper(self):
        """ Разделяет большой файл на несколько файлов, записывая их в папку temp_directory. 
        Если такой папки нет, то она будет создана.
        Внутри каждого кусочка значения разделяются переносом строки и сортируются в соответствии с параметрами.
        Размер одного кусочка не меньше, чем size_of_one_piece байт.
                    
        Raises:
            RuntimeError: если папка для временных файлов оказалась непуста. 
        """
        LOGGER.info('Mapper is start.')
        if not isinstance(self.reverse, bool):
            raise TypeError("flag reverse must be a bool, but got {0}:{1}".format(type(self.reverse), self.reverse))

        try:
            utils.check_directory_path(self.temp_directory)
        except FileNotFoundError:
            LOGGER.info("Directory for temp files is not found. Creating this...")
            os.makedirs(self.temp_directory)

        if len(os.listdir(self.temp_directory)) > 0:
            raise RuntimeError("{0} папка не пуста!".format(self.temp_directory))

        with open(self.input_filename, 'r') if self.input_filename is not None else sys.stdin as source_file:
            LOGGER.info('Mapping...')
            if self.size_of_one_piece is None:
                self.size_of_one_piece = psutil.virtual_memory().free // 10  # этот размер с должен влезать в память
                LOGGER.info("Size of one piece file chosen as {0}.".format(self.size_of_one_piece))
            while True:
                piece_data = utils.get_next_data_piece(source_file, self.size_of_one_piece, self.separator)
                if len(piece_data) == 0:
                    LOGGER.info('Reached the end of file.')
                    break
                piece_data = self.separator.join(
                    sorted(piece_data.split(self.separator), reverse=self.reverse, key=self.key_sort_piece))
                self.pieces.append(
                    piece.Piece(len(self.pieces), piece_data, self.temp_directory))
        LOGGER.info('Mapping is done!')

    def reducer(self):
        """ Сливает много отсортированных файлов обратно в 1 файл. 
        Среди всех кусков смотрится верхний еще не добавленный в файл элемент, и из них выбирается экстремум - 
        наибольший или наименьший элемент, в зависимости от настройки алгоритма, а в соответствующем куске указатель
        на верхний элемент сдвигается на следующий после него элемент. Если кусок прочитан до конца, то он становится 
        None. Алгоритм заканчивает свою работу, когда все кусочки были дочитаны до конца, то есть стали None.
        """
        LOGGER.info('Reducer is  start...')
        with open(self.output_filename, 'w') if self.output_filename is not None else sys.stdout as output:
            while True:
                LOGGER.info("Let's find an extremum among pieces.")
                extr = None                 # Найдем экстремум.
                for piece in self.pieces:
                    if piece is None:
                        continue
                    element = piece.get_up_element(self.temp_directory, self.separator)
                    # костыль
                    expression = extr is None or self.key_sort_piece(extr.data) < self.key_sort_piece(element) if \
                        self.reverse else extr is None or self.key_sort_piece(extr.data) > self.key_sort_piece(element)
                    if expression:
                        extr = extremum.Extremum(element, piece)

                if extr is None or extr.data is None:
                    LOGGER.info("All of pieces is empty.")
                    break
                LOGGER.info("Extremum is {0}".format(extr.data))
                # экстремум найден, теперь его нужно удалить из соответствующего файла и положить в output.
                output.write(extr.data + self.separator)
                extr.piece_obj.delete_up_element(self.temp_directory, self.separator)
                if extr.piece_obj.is_empty(self.temp_directory):
                    self.pieces[extr.piece_obj.index] = None
        LOGGER.info('Reducing is done!')

    def clean_up(self, is_debug=False):
        if not is_debug:
            shutil.rmtree(self.temp_directory)
            LOGGER.info("Delete temp files.")
