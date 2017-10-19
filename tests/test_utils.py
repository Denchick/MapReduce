import unittest
import os
import sys

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                             os.path.pardir))
from map_reduce import utils


class TestUtils(unittest.TestCase):
    def setUp(self):
        self.filename = 'temp.txt'

    def tearDown(self):
        if os.path.exists(self.filename):
            os.remove(self.filename)

    def test_comparator(self):
        exp = utils.comparator(10, 10)
        self.assertEqual(exp, 0)
        # на равные элементы реверс не действует
        exp = utils.comparator(10, 10, reverse=True)
        self.assertEqual(exp, 0)
        exp = utils.comparator(-2, 2)
        self.assertEqual(exp, -1)

        exp = utils.comparator('kek', 'kek')
        self.assertEqual(exp, 0)
        # Работает с кириллицей
        exp = utils.comparator('лол', 'лол')
        self.assertEqual(exp, 0)
        # Работает даже с иероглифами
        exp = utils.comparator('彐丅口 中认闩匚片口, 石卩闩丅闩卄', '彐丅口 中认闩匚片口, 石卩闩丅闩卄')
        self.assertEqual(exp, 0)
        # лексикографическое сравнение строк
        exp = utils.comparator('abc', 'abd')
        self.assertEqual(exp, -1)
        # в обратном порядке
        exp = utils.comparator('abc', 'abd', reverse=True)
        self.assertEqual(exp, 1)
        # длина строк
        exp = utils.comparator('aaa', 'a')
        self.assertEqual(exp, 1)
        # Регистро-зависимая
        exp = utils.comparator('AB', 'ab', case_sensitive=True)
        self.assertEqual(exp, -1)
        # Регистро-независимая
        exp = utils.comparator('AB', 'ab', case_sensitive=False)
        self.assertEqual(exp, 0)

    def test_get_next_data_piece(self):
        def pattern_for_testing_without_exceptions(data, separator, count, expected):
            with open(self.filename, 'w') as f:
                f.write(separator.join(data))
            with open(self.filename, 'r') as f:
                result = utils.get_next_data_piece(f, count, separator)
                self.assertEqual(result, expected)

        def pattern_for_testing_with_exceptions(data, separator, count, error_type):
            sep = ';' if not isinstance(separator, str) else separator
            with open(self.filename, 'w') as f:
                f.write(sep.join(data))
            with open(self.filename, 'r') as f:
                with self.assertRaises(error_type):
                    utils.get_next_data_piece(f, count, separator)

        pattern_for_testing_without_exceptions(['kek', 'cheburek'], ';', 3, 'kek')
        pattern_for_testing_without_exceptions(['kek', 'cheburek'], ';', 4, 'kek')
        pattern_for_testing_without_exceptions(['kek', 'cheburek'], ';', 5, 'kek;cheburek')
        pattern_for_testing_without_exceptions(['kek'], ';', 4, 'kek')
        pattern_for_testing_without_exceptions(['kek', 'cheburek'], ';', 20, 'kek;cheburek')

        pattern_for_testing_with_exceptions(['kek'], ';', '401', TypeError)
        pattern_for_testing_with_exceptions(['kek'], True, 2, TypeError)
        with self.assertRaises(AttributeError):
            utils.get_next_data_piece('not_file', 10, '\n')


if __name__ == "__main__":
    unittest.main()
