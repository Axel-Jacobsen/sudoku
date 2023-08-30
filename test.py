#! /usr/bin/env python3
import unittest

from sudoku import Sudoku, solve


class SudokuBoardTest(unittest.TestCase):
    def test_basic_valid_1(self):
        s = Sudoku()
        s.set_grid(
            [
                [1, 2, 3, 4, 5, 6, 7, 8, 9],
                [4, 5, 6, 7, 8, 9, 1, 2, 3],
                [7, 8, 9, 1, 2, 3, 4, 5, 6],
                [2, 3, 4, 5, 6, 7, 8, 9, 1],
                [5, 6, 7, 8, 9, 1, 2, 3, 4],
                [8, 9, 1, 2, 3, 4, 5, 6, 7],
                [3, 4, 5, 6, 7, 8, 9, 1, 2],
                [6, 7, 8, 9, 1, 2, 3, 4, 5],
                [9, 1, 2, 3, 4, 5, 6, 7, 8],
            ]
        )
        self.assertTrue(s.check_valid())

    def test_basic_valid_2(self):
        s = Sudoku()
        s.set_grid(
            [
                [4, 2, 8, 1, 7, 3, 6, 9, 5],
                [7, 3, 9, 5, 6, 2, 8, 4, 1],
                [5, 6, 1, 9, 8, 4, 7, 3, 2],
                [3, 5, 4, 6, 2, 8, 1, 7, 9],
                [9, 8, 7, 3, 5, 1, 2, 6, 4],
                [6, 1, 2, 7, 4, 9, 5, 8, 3],
                [2, 7, 5, 4, 9, 6, 3, 1, 8],
                [1, 9, 6, 8, 3, 5, 4, 2, 7],
                [8, 4, 3, 2, 1, 7, 9, 5, 6],
            ]
        )
        self.assertTrue(s.check_valid())

    def test_basic_invalid_1(self):
        s = Sudoku()
        s.set_grid(
            [
                [1, 2, 3, 4, 5, 6, 7, 8, 9],
                [4, 5, 6, 7, 8, 9, 1, 2, 3],
                [7, 8, 9, 1, 2, 3, 4, 5, 6],
                [2, 3, 4, 5, 6, 7, 8, 9, 1],
                [5, 6, 7, 8, 9, 1, 2, 3, 4],
                [8, 9, 1, 2, 3, 4, 5, 6, 7],
                [3, 4, 5, 6, 7, 8, 9, 1, 2],
                [6, 7, 8, 9, 1, 2, 3, 4, 5],
                [9, 1, 2, 3, 4, 5, 6, 7, 1],
            ]
        )
        self.assertFalse(s.check_valid())

    def test_basic_invalid_2(self):
        s = Sudoku()
        s.set_grid(
            [
                [1, 2, 8, 1, 7, 3, 6, 9, 5],
                [7, 3, 9, 5, 6, 2, 8, 4, 1],
                [5, 6, 1, 9, 8, 4, 7, 3, 2],
                [3, 5, 4, 6, 2, 8, 1, 7, 9],
                [9, 8, 7, 3, 5, 1, 2, 6, 4],
                [6, 1, 2, 7, 4, 9, 5, 8, 3],
                [2, 7, 5, 4, 9, 6, 3, 1, 8],
                [1, 9, 6, 8, 3, 5, 4, 2, 7],
                [8, 4, 3, 2, 1, 7, 9, 5, 6],
            ]
        )
        self.assertFalse(s.check_valid())

    def test_incomplete_1(self):
        s = Sudoku()
        s.set_grid(
            [
                [1, 2, 8, 1, 7, 3, 6, 9, 5],
                [7, 3, 9, 5, 6, 2, 8, 4, 1],
                [5, 6, 1, 9, 8, 4, 7, 3, 2],
                [3, 5, 4, 6, 2, 8, 1, 7, 9],
                [9, 8, 7, 3, 5, 1, 2, 6, 4],
                [6, 1, 2, 7, 4, 9, 5, 8, 3],
                [2, 7, 5, 4, 9, 6, 3, 1, 8],
                [1, 9, 6, 8, 3, 5, 4, 2, 7],
                [8, 4, 3, 2, 1, 7, 9, 5, None],
            ]
        )
        self.assertFalse(s.check_valid())

    def test_basic_solve_1(self):
        s = Sudoku()
        s.set_grid(
            [
                [1, 2, 3, 4, 5, 6, 7, 8, 9],
                [4, 5, 6, 7, 8, 9, 1, 2, 3],
                [7, 8, 9, 1, 2, 3, 4, 5, 6],
                [2, 3, 4, 5, 6, 7, 8, 9, 1],
                [5, 6, 7, 8, 9, 1, 2, 3, 4],
                [8, 9, 1, 2, 3, 4, 5, 6, 7],
                [3, 4, 5, 6, 7, 8, 9, 1, 2],
                [6, 7, 8, 9, 1, 2, 3, 4, 5],
                [9, 1, 2, 3, 4, 5, 6, 7, None],
            ]
        )
        truth = Sudoku()
        truth.set_grid(
            [
                [1, 2, 3, 4, 5, 6, 7, 8, 9],
                [4, 5, 6, 7, 8, 9, 1, 2, 3],
                [7, 8, 9, 1, 2, 3, 4, 5, 6],
                [2, 3, 4, 5, 6, 7, 8, 9, 1],
                [5, 6, 7, 8, 9, 1, 2, 3, 4],
                [8, 9, 1, 2, 3, 4, 5, 6, 7],
                [3, 4, 5, 6, 7, 8, 9, 1, 2],
                [6, 7, 8, 9, 1, 2, 3, 4, 5],
                [9, 1, 2, 3, 4, 5, 6, 7, 8],
            ]
        )
        self.assertTrue(s.check_valid())
        solved = solve(s)
        self.assertTrue(solved.check_valid())
        self.assertEqual(solved, truth)

    def test_basic_solve_2(self):
        s = Sudoku()
        s.set_grid(
            [
                [None, None, 8, 1, 7, 3, None, None, None],
                [7, 3, 9, 5, 6, 2, 8, 4, 1],
                [5, 6, 1, 9, 8, 4, 7, 3, 2],
                [3, 5, 4, 6, 2, 8, 1, 7, 9],
                [9, 8, 7, 3, 5, 1, 2, 6, 4],
                [6, 1, 2, 7, 4, 9, 5, 8, 3],
                [2, 7, 5, 4, 9, 6, 3, None, None],
                [1, 9, 6, 8, 3, 5, 4, None, None],
                [8, 4, 3, 2, 1, 7, 9, None, None],
            ]
        )
        truth = Sudoku()
        truth.set_grid(
            [
                [4, 2, 8, 1, 7, 3, 6, 9, 5],
                [7, 3, 9, 5, 6, 2, 8, 4, 1],
                [5, 6, 1, 9, 8, 4, 7, 3, 2],
                [3, 5, 4, 6, 2, 8, 1, 7, 9],
                [9, 8, 7, 3, 5, 1, 2, 6, 4],
                [6, 1, 2, 7, 4, 9, 5, 8, 3],
                [2, 7, 5, 4, 9, 6, 3, 1, 8],
                [1, 9, 6, 8, 3, 5, 4, 2, 7],
                [8, 4, 3, 2, 1, 7, 9, 5, 6],
            ]
        )
        self.assertTrue(s.check_valid(verbose=True))
        solved = solve(s)
        self.assertTrue(solved.check_valid())
        self.assertEqual(solved, truth)

    def test_performance_solve_1(self):
        s = Sudoku()
        s.set_grid(
            [
                [None, None, 8, None, None, 3, None, None, None],
                [None, None, 9, None, 6, 2, None, 4, 1],
                [None, None, 1, 9, None, None, None, None, 2],
                [None, 5, None, None, 2, None, None, 7, 9],
                [None, None, 7, None, None, None, 2, None, None],
                [6, 1, None, None, 4, None, None, 8, None],
                [2, None, None, None, None, 6, 3, None, None],
                [1, 9, None, 8, 3, None, 4, None, None],
                [None, None, None, 2, None, None, 9, None, None],
            ]
        )
        truth = Sudoku()
        truth.set_grid(
            [
                [4, 2, 8, 1, 7, 3, 6, 9, 5],
                [7, 3, 9, 5, 6, 2, 8, 4, 1],
                [5, 6, 1, 9, 8, 4, 7, 3, 2],
                [3, 5, 4, 6, 2, 8, 1, 7, 9],
                [9, 8, 7, 3, 5, 1, 2, 6, 4],
                [6, 1, 2, 7, 4, 9, 5, 8, 3],
                [2, 7, 5, 4, 9, 6, 3, 1, 8],
                [1, 9, 6, 8, 3, 5, 4, 2, 7],
                [8, 4, 3, 2, 1, 7, 9, 5, 6],
            ]
        )
        self.assertTrue(s.check_valid(verbose=True))
        solved = solve(s)
        self.assertTrue(solved.check_valid())
        self.assertEqual(solved, truth)


if __name__ == "__main__":
    unittest.main()
