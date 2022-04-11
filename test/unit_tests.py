import unittest
from src.new_solve import *
import os


class EasyTestCases(unittest.TestCase):
    def test_simple(self):
        self.assertEqual(
            Cnf(pars_file("../input/input.txt")).get_solution(), []
        )

    def test_simple1(self):
        self.assertNotEqual(
            Cnf(pars_file("../input/input1.txt")).get_solution(), []
        )

    def test_simple2(self):
        self.assertNotEqual(
            Cnf(pars_file("../input/input2.txt")).get_solution(), []
        )

    def test_simple3(self):
        self.assertNotEqual(
            Cnf(pars_file("../input/input3.txt")).get_solution(), []
        )


class HardTestCases(unittest.TestCase):
    def test_hard1(self):
        self.assertNotEqual(
            Cnf(pars_file("../input/input4.txt")).get_solution(), []
        )

    def test_hard2(self):
        self.assertNotEqual(
            Cnf(pars_file("../input/input5.txt")).get_solution(), []
        )

    def test_hard3(self):
        self.assertNotEqual(
            Cnf(pars_file("../input/input6.txt")).get_solution(), []
        )

    def test_hard4(self):
        self.assertEqual(
            Cnf(pars_file("../input/input7.txt")).get_solution(), []
        )


class UniformTestCases(unittest.TestCase):
    def test_uniform_all_sat(self):
        for filename in os.listdir('../uniform_test/sat'):
            self.assertNotEqual(
                Cnf(pars_file(os.path.join('../uniform_test/sat', filename))).get_solution(), []
            )

    def test_uniform_all_unsat(self):
        for filename in os.listdir('../uniform_test/unsat'):
            self.assertEqual(
                Cnf(pars_file(os.path.join('../uniform_test/unsat', filename))).get_solution(), []
            )


if __name__ == '__main__':
    unittest.main()
