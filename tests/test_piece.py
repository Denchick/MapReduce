import unittest

from 

class TestPiece(unittest.TestCase):
    def setUp(self):
        print("setUp")
        self.n = 10

    def tearDown(self):
        print("tearDown")
        del self.n

    # @classmethod
    # def setUpClass(cls):
    #     print("setUpClass")
    #
    # @classmethod
    # def tearDownClass(cls):
    #     print("tearDownClass")
    #
    # def test_fib_assert_equal(self):
    #     self.assertEqual(fib(self.n), 55)
    #
    # def test_fib_assert_true(self):
    #     self.assertTrue(fib(self.n) == 55)


if __name__ == "__main__":
    unittest.main()
