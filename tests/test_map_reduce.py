import unittest
import shutil
import os
import sys
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                             os.path.pardir))

from map_reduce import map_reduce


class TestMapReduce(unittest.TestCase):
    def setUp(self):
        """ Создает в папке temp файлы для тестов """
        self.directory = 'temp_test'
        os.mkdir(self.directory)

        self.input_filename = 'input_test.txt'
        self.output_filename = 'output_test.txt'

        self.separator = ' '
        self.count = 20

    def tearDown(self):
        """ Удаляет папку temp со всем содержимым и файлы входа и выхода"""
        shutil.rmtree(self.directory, ignore_errors=False, onerror=None)
        os.remove(self.input_filename)
        os.remove(self.output_filename)

    def get_data_from_file(self, file):
        with open(file, 'r') as f:
            return f.read().strip()

    def create_file_for_sorting(self, data):
        """ Создает тестовый файл для сортировки
        
        Args:
            data (str): строка - данные, которые нужно записать в файл
        """
        with open(self.input_filename, 'w') as f:
            f.write(data)

    def test_correctSort_whenPieceSizeLessThanAllocatedMemory(self):
        data = '4 1 3 2'
        self.create_file_for_sorting(data)

        map_reduce.MapReduce(
            input_filename=self.input_filename,
            output_filename=self.output_filename,
            separator=' ',
            temp_directory=self.directory,
            size_of_one_piece=10,
            reverse=False,
            debug=False)

        actual = self.get_data_from_file(self.output_filename)
        self.assertEqual('1 2 3 4', actual)

    def test_correctSort_whenFileDivideIntoTwoPieces(self):
        data = '4 1 3 2'
        self.create_file_for_sorting(data)

        map_reduce.MapReduce(
            input_filename=self.input_filename,
            output_filename=self.output_filename,
            separator=' ',
            temp_directory=self.directory,
            size_of_one_piece=4,
            reverse=False,
            debug=False)

        actual = self.get_data_from_file(self.output_filename)
        self.assertEqual('1 2 3 4', actual)

    def test_correct_thatNumbersNotRecognizedAdStrings(self):
        data = '11 1 2'
        self.create_file_for_sorting(data)

        map_reduce.MapReduce(
            input_filename=self.input_filename,
            output_filename=self.output_filename,
            separator=' ',
            temp_directory=self.directory,
            size_of_one_piece=100,
            reverse=False,
            debug=False)

        actual = self.get_data_from_file(self.output_filename)
        self.assertEqual('1 2 11', actual)

    def test_correctSort_lenghtInputFileAndOutputFileAreEquals(self):
        data = '18 20 4 2 19 5 16 14 1 17 6 13 10 15 8 3 11 12 7 9'
        self.create_file_for_sorting(data)

        map_reduce.MapReduce(
            input_filename=self.input_filename,
            output_filename=self.output_filename,
            separator=' ',
            temp_directory=self.directory,
            size_of_one_piece=5,
            reverse=False,
            debug=False)

        expected = '1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20'
        actual = self.get_data_from_file(self.output_filename)
        self.assertEqual(expected, actual)

    def test_correctSort_thanReverse(self):
        data = '4 1 3 2'
        self.create_file_for_sorting(data)

        map_reduce.MapReduce(
            input_filename=self.input_filename,
            output_filename=self.output_filename,
            separator=' ',
            temp_directory=self.directory,
            size_of_one_piece=4,
            reverse=True,
            debug=False)

        actual = self.get_data_from_file(self.output_filename)
        self.assertEqual('4 3 2 1', actual)



if __name__ == "__main__":
    unittest.main()
