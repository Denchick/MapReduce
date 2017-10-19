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
        self.directory = 'temp'
        self.source_filename = 'source'
        os.mkdir(self.directory)

    def tearDown(self):
        """ Удаляет папку temp со всем содержимым """
        shutil.rmtree(self.directory, ignore_errors=False, onerror=None)

    def test_pieces_is_empty(self):
        pass

    def test_mapper(self):
        data = ['first', 'second', 'third']
        separator = ' '
        with open('temp.txt') as f:
            f.write(separator.join(data))
        m = map_reduce.MapReduce('te')

    def test_reducer(self):
        pass


if __name__ == "__main__":
    unittest.main()
