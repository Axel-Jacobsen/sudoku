#! /usr/bin/env python3

import unittest

from copy import deepcopy
from typing import List, Tuple, Optional


class Sudoku:
    def __init__(self):
        self.grid: List[List[Optional[int]]] = [
            [None for i in range(9)] for j in range(9)
        ]

    def copy(self) -> "Sudoku":
        s = Sudoku()
        s.set_grid(deepcopy(self.grid))
        return s

    def __eq__(self, other: object) -> bool:
        # todo impl Sudoku eq grids, not just Sudoku eq Sudoku
        if not isinstance(other, type(self)):
            return False
        return self.grid == other.grid

    def __getitem__(self, i: int, j: int) -> Optional[int]:
        return self.grid[i][j]

    def __setitem__(self, pos: Tuple[int, int], val: int) -> None:
        i, j = pos
        self.grid[i][j] = val

    def __repr__(self) -> str:
        rows: List[str] = []
        for row in self.grid:
            string_els: List[str] = [str(el) if el is not None else "_" for el in row]
            rows.append(" ".join(string_els))
        board = "\n".join(rows)
        return board

    def set_grid(self, grid: List[List[Optional[int]]]) -> None:
        self.grid = grid

    def check_elements(self, els: List[Optional[int]]) -> bool:
        unsolved_adjustment = els.count(None) - 1 if els.count(None) > 1 else 0
        return len(set(els)) + unsolved_adjustment == len(els)

    def check_row(self, row: int) -> bool:
        """
        a row is valid iff
        - all elements are 1..9 or None
        - there are no repeat numbers in the row
        """
        if not (0 <= row < 9):
            raise ValueError(f"row index {row} out of bounds")

        return self.check_elements(self.grid[row])

    def check_col(self, col: int) -> bool:
        if not (0 <= col < 9):
            raise ValueError(f"column index {col} out of bounds")

        return self.check_elements([self.grid[i][col] for i in range(9)])

    def check_square(self, row: int, col: int) -> bool:
        if not (0 <= row < 3 and 0 <= col < 3):
            raise ValueError(f"square index ({row}, {col}) out of bounds")

        els = [self.grid[3 * row + i][3 * col + j] for i in range(3) for j in range(3)]
        return self.check_elements(els)

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

    for candidate in range(1, 10):
        board[row, col] = candidate
        if board.check_solved():
            return board

        if board.check_valid():
            candidate_board = solve(board)
            if candidate_board is not None:
                return candidate_board

    board[row, col] = None
    return None  # no valid solutions
