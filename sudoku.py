#! /usr/bin/env python3

import numpy as np

from copy import deepcopy
from typing import Any, List, Tuple, Union, Optional


class Board:
    def __init__(self):
        self.grid: List[List[Optional[int]]] = [
            [None for i in range(9)] for j in range(9)
        ]

    def __eq__(self, other: object) -> bool:
        # TODO impl Board eq grids, not just Board eq Board
        if not isinstance(other, type(self)):
            return False
        return self.grid == other.grid

    def __getitem__(self, *args) -> Any:
        # TODO how do you write and type numpy-style indexing?
        return self.grid.__getitem__(*args)

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

    def copy(self) -> "Board":
        s = Board()
        s.set_grid(deepcopy(self.grid))
        return s

    def set_grid(self, grid: List[List[Optional[int]]]) -> None:
        self.grid = grid


class Sudoku:
    def __init__(
        self, board: Union[List[List[Optional[int]]], np.ndarray, Board]
    ) -> None:
        if isinstance(board, Board):
            self._board = board
        else:
            self._board = Board()
            assert isinstance(
                board, list
            ), f"not implemented board for type {type(board)}"
            self._board.set_grid(board)  # type: ignore

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, type(self)):
            return False
        return self._board == other._board

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

        return self.check_elements(self._board[row])

    def check_col(self, col: int) -> bool:
        if not (0 <= col < 9):
            raise ValueError(f"column index {col} out of bounds")

        return self.check_elements([self._board[i][col] for i in range(9)])

    def check_square(self, row: int, col: int) -> bool:
        if not (0 <= row < 3 and 0 <= col < 3):
            raise ValueError(f"square index ({row}, {col}) out of bounds")

        els = [
            self._board[3 * row + i][3 * col + j] for i in range(3) for j in range(3)
        ]
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

    def get_empty_grid_positions(self) -> List[Tuple[int, int]]:
        return [(i, j) for i in range(9) for j in range(9) if self._board[i][j] is None]

    def find_gimme_at(self, row: int, col: int) -> Optional[int]:
        """a "gimme" is a spot in the sudoku _board that has exactly 1 possible
        number, given the current _board

        multiple ways we can determine this (and this will be incomplete):
            - if an empty square is in a row/col/square with 8 numbers,
            it is the last number
            - some other ways that i'll implement later
        """
        square_row, square_col = row // 3, col // 3
        row_numbers = set(self._board[row]) - {None}
        col_numbers = set([self._board[i][col] for i in range(9)]) - {None}
        square_numbers = set(
            [
                self._board[3 * square_row + i][3 * square_col + j]
                for i in range(3)
                for j in range(3)
            ]
        ) - {None}

        gimme = set(range(1, 10)) - row_numbers - col_numbers - square_numbers
        if len(gimme) == 1:
            return gimme.pop()
        return None

    def find_gimmes(self) -> List[Tuple[Tuple[int, int], int]]:
        empty__board_positions = self.get_empty_grid_positions()
        gimmes = []
        for row, col in empty__board_positions:
            gimme = self.find_gimme_at(row, col)
            if gimme is not None:
                gimmes.append(((row, col), gimme))
        return gimmes

    def solve(self) -> Optional["Sudoku"]:
        """
        There is a nice recursive solution here:

        pick the first empty slot
        for numbers in 1..9
            if it is valid, try solve with new grid
                if solve with new grid returns a board, return board
                else, continue
            if it is invalid, continue
        return false

        On top of that, you can add stuff to make this brute force faster,
        such as searching for naked or hidden singles. Beyond that, there
        is some constraint satisfaction stuff that I don't understand yet.

        Note: I think the separation between board and solver here is a bit
        finicky still, and I probably have the wrong abstraction right now
        """
        gimmes = self.find_gimmes()
        if len(gimmes) > 0:
            for (row, col), gimme in gimmes:
                self._board[row, col] = gimme

        if self.check_solved():
            return self

        row, col = self.get_empty_grid_positions().pop()

        for candidate in range(1, 10):
            self._board[row, col] = candidate
            if self.check_solved():
                return self

            if self.check_valid():
                candidate_self = self.solve()
                if candidate_self is not None:
                    return candidate_self

        self._board[row, col] = None  # type: ignore
        for (row, col), _ in gimmes:
            self._board[row, col] = None  # type: ignore
        return None  # no valid solutions
