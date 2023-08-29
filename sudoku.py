#! /usr/bin/env python3

import unittest

from copy import deepcopy
from typing import List, Tuple, Optional


class Sudoku:
    def __init__(self):
        self.grid: List[List[Optional[int]]] = [
            [None for i in range(9)] for j in range(9)
        ]

    def copy(self):
        s = Sudoku()
        s.set_grid(deepcopy(self.grid))

    def __getitem__(self, i: int, j: int) -> Optional[int]:
        return self.grid[i][j]

    def __setitem__(self, pos: Tuple[int,int], val: int) -> None:
        i,j = pos
        self.grid[i][j] = val

    def set_grid(self, grid: List[List[Optional[int]]]) -> None:
        self.grid = grid

    def check_row(self, row: int) -> bool:
        if not (0 <= row < 9):
            raise ValueError(f"row index {row} out of bounds")

        return set(range(1, 10)) - set(self.grid[row]) == set()

    def check_col(self, col: int) -> bool:
        if not (0 <= col < 9):
            raise ValueError(f"column index {col} out of bounds")

        return set(range(1, 10)) - set([self.grid[i][col] for i in range(9)]) == set()

    def check_square(self, row: int, col: int) -> bool:
        if not (0 <= row < 3 and 0 <= col < 3):
            raise ValueError(f"square index ({row}, {col}) out of bounds")

        elements = [
            self.grid[3 * row + i][3 * col + j] for i in range(3) for j in range(3)
        ]
        return set(range(1, 10)) - set(elements) == set()

    def check_valid(self) -> bool:
        for i in range(9):
            if not self.check_row(i) or not self.check_col(i):
                return False
        for i in range(3):
            for j in range(3):
                if not self.check_square(i, j):
                    return False
        return True

    def check_solved(self) -> bool:
        return self.check_valid() and len(self.get_empty_grid_positions()) == 0

    def get_empty_grid_positions(self) -> List[List[int]]:
        return [[i, j] for i in range(9) for j in range(9) if self.grid[i][j] is None]

def solve(board) -> Optional["Sudoku"]:
    """
    There is a nice recursive solution here

    while not solved:
        pick the first empty slot
        for numbers in 1..9
            if it is valid, try solve with new grid
                if solve with new grid returns a board, return board
                else, continue
            if it is invalid, continue
        return false
    """
    if board.check_solved():
        return board

    row, col = board.get_empty_grid_positions().pop()
    for candidate in range(1,10):
        board[row, col] = candidate
        if board.check_valid():
            copy = board.copy()
            candidate_board = copy.solve()
            if candidate_board is not None:
                return candidate_board
    return None  # no valid solutions


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
        solved = solve(s)
        self.assertTrue(solved.check_valid())

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
        solved = solve(s)
        self.assertTrue(solved.check_valid())


if __name__ == "__main__":
    unittest.main()
