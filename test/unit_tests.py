import unittest
from src.new_solve import *


class EasyTestCases(unittest.TestCase):
    def test_simple(self):
        self.assertEqual(
            Cnf(pars_file("../input/input.txt")).get_solution(), []
        )

    def test_simple1(self):
        self.assertIsNot(
            Cnf(pars_file("../input/input1.txt")).get_solution(), []
        )

    def test_simple2(self):
        self.assertIsNot(
            Cnf(pars_file("../input/input2.txt")).get_solution(), []
        )

    def test_simple3(self):
        self.assertEqual(
            Cnf(pars_file("../input/input3.txt")).get_solution(), [1, 2]
        )


class HardTestCases(unittest.TestCase):
    def test_hard1(self):
        self.assertIsNot(
            Cnf(pars_file("../input/input4.txt")).get_solution(), []
        )

    def test_hard2(self):
        self.assertIsNot(
            Cnf(pars_file("../input/input5.txt")).get_solution(), []
        )

    def test_hard3(self):
        self.assertIsNot(
            Cnf(pars_file("../input/input6.txt")).get_solution(), []
        )


if __name__ == '__main__':
    unittest.main()
