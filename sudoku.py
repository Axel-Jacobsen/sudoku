#! /usr/bin/env python3

from typing import List


class Sudoku:
    def __init__(self):
        self.grid = [[None for i in range(9)] for j in range(9)]

    def set_grid(self, grid: List[List[int]]) -> None:
        self.grid = grid

    def check_row(self, row: int) -> bool:
        if not (0 <= row < 9):
            raise ValueError(f"row index {row} out of bounds")

        return set(self.grid[row]) == set(range(1, 10))

    def check_col(self, col: int) -> bool:
        if not (0 <= col < 9):
            raise ValueError(f"column index {col} out of bounds")

        return set([self.grid[i][col] for i in range(9)]) == set(range(1, 10))

    def check_square(self, row: int, col: int) -> bool:
        if not (0 <= row < 3 and 0 <= col < 3):
            raise ValueError(f"square index ({row}, {col}) out of bounds")

        return set(
            [
                self.grid[3 * row + i][3 * col + j]
                for i in range(3)
                for j in range(3)
            ]
        ) == set(range(1, 10))

    def check_valid(self) -> bool:
        for i in range(9):
            if not self.check_row(i) or not self.check_col(i):
                return False
        for i in range(3):
            for j in range(3):
                if not self.check_square(i, j):
                    return False
        return True
