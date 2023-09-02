#! /usr/bin/env python3


import numpy as np

from typing import List, Tuple, Union, Optional


class Sudoku:
    """
    0 represents "no number"
    1-9 are the numbers!
    """

    def __init__(self):
        self.grid = np.zeros((9, 9), dtype=np.uint8)

    def copy(self) -> "Sudoku":
        s = Sudoku()
        s.set_grid(self.grid.copy())
        return s

    def __eq__(self, other: object) -> bool:
        # todo impl Sudoku eq grids, not just Sudoku eq Sudoku
        if not isinstance(other, type(self)):
            return False
        return (self.grid == other.grid).all()

    def __getitem__(self, *args) -> Union[np.ndarray, int]:
        return self.grid.__getitem__(*args)

    def __setitem__(self, pos: Tuple[int, int], val: int) -> None:
        i, j = pos
        self.grid[i, j] = val

    def __repr__(self) -> str:
        rows: List[str] = []
        for row in self.grid:
            string_els: List[str] = [str(el) if el is not None else "_" for el in row]
            rows.append(" ".join(string_els))
        board = "\n".join(rows)
        return board

    def _np_arr_to_set(self, arr: np.ndarray) -> set:
        return set(arr.flatten())

    def set_grid(self, grid: Union[np.ndarray, List[List[Optional[int]]]]) -> None:
        if isinstance(grid, list):
            # assume list of list of optional int
            grid = np.array(
                [[0 if el is None else int(el) for el in row] for row in grid]
            )

        self.grid = grid

    def check_elements(self, els: np.ndarray) -> bool:
        num_unsolved_squares = (els == 0).sum()
        unsolved_adjustment = (
            num_unsolved_squares - 1 if num_unsolved_squares > 1 else 0
        )
        return len(self._np_arr_to_set(els)) + unsolved_adjustment == len(els)

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

        return self.check_elements(self.grid[:, col])

    def check_square(self, row: int, col: int) -> bool:
        if not (0 <= row < 3 and 0 <= col < 3):
            raise ValueError(f"square index ({row}, {col}) out of bounds")

        square = self.grid[3 * row : 3 * row + 3, 3 * col : 3 * col + 3]
        square = square.flatten()
        return self.check_elements(square)

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
        return list(zip(*np.where(self.grid == 0)))  # type: ignore

    def find_gimme_at(self, row: int, col: int) -> Optional[int]:
        """a "gimme" is a spot in the sudoku grid that has exactly 1 possible
        number, given the current grid

        multiple ways we can determine this (and this will be incomplete):
            - if an empty square is in a row/col/square with 8 numbers,
            it is the last number
            - some other ways that i'll implement later

        in sudoku circles, this is "naked single"
        """
        square_row, square_col = row // 3, col // 3
        row_numbers = self._np_arr_to_set(self.grid[row]) - {0}
        col_numbers = self._np_arr_to_set(self.grid[:, col]) - {0}

        square = self.grid[
            3 * square_row : 3 * (square_row + 1), 3 * square_col : 3 * (square_col + 1)
        ]
        square_numbers = self._np_arr_to_set(square) - {0}

        gimme = set(range(1, 10)) - row_numbers - col_numbers - square_numbers

        if len(gimme) == 1:
            return gimme.pop()

        return None

    def find_gimmes(self) -> List[Tuple[Tuple[int, int], int]]:
        empty_grid_positions = self.get_empty_grid_positions()
        gimmes = []
        for row, col in empty_grid_positions:
            gimme = self.find_gimme_at(row, col)
            if gimme is not None:
                gimmes.append(((row, col), gimme))
        return gimmes


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
    gimmes = board.find_gimmes()
    if len(gimmes) > 0:
        for (row, col), gimme in gimmes:
            board[row, col] = gimme

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

    # reset the board
    board[row, col] = 0
    for (row, col), _ in gimmes:
        board[row, col] = 0

    return None  # no valid solutions
