#! /usr/bin/env python3

"""
Parse puzzles from the Sudoku forum database. They are in the form of
12...4.5..... etc for 81 characters, row major.
"""

import time

from pathlib import Path
from copy import deepcopy
from typing import List, Optional

from sudoku import Sudoku, solve


DEFAULT_PUZZLES = Path(__file__).parent / "puzzles" / "ph_2010" / "02_index.txt"


class PuzzleParser:
    def __init__(self, puzzle_path: Path = DEFAULT_PUZZLES) -> None:
        """
        3,103,972 puzzles are ~277 MB, so just load them into memory

        Note: not suitable for multiprocessing yet, as we are using object arrays
        """
        with open(puzzle_path, "r") as f:
            raw_puzzle_string = f.read()
            puzzles = PuzzleParser._process_raw_puzzles(raw_puzzle_string)

        self._puzzles = puzzles
        self._idx: Optional[int] = None

    def __getitem__(self, idx: int) -> List[List[Optional[int]]]:
        puzzle = self._puzzles[idx]
        return [puzzle[9 * i : 9 * i + 9] for i in range(9)]

    def __len__(self) -> int:
        return len(self._puzzles)

    def __iter__(self) -> "PuzzleParser":
        self._idx = 0
        return self

    def __next__(self) -> List[List[Optional[int]]]:
        if self._idx is None:
            raise TypeError("need to `iter` the puzzle parser")

        self._idx += 1

        if self._idx == len(self):
            raise StopIteration

        return self[self._idx]

    @staticmethod
    def _process_raw_puzzles(puzzles_string: str) -> List[List[Optional[int]]]:
        puzzles_by_line = puzzles_string.strip().split("\n")

        # filter out indexes
        puzzles_by_line = [puzz.split(";")[0] for puzz in puzzles_by_line]

        # process into something that we can make into a np array
        preprocessed_puzzles = [
            [None if c == "." else int(c) for c in puzzle_string]
            for puzzle_string in puzzles_by_line
        ]

        return preprocessed_puzzles


if __name__ == "__main__":
    print("loading puzzles...")
    t0 = time.perf_counter()
    PP = PuzzleParser()
    t1 = time.perf_counter()
    print(f"loaded {len(PP)} puzzles in {t1 - t0:.3f} s")

    ts: List[float] = []
    s = Sudoku()

    for i, puzz in enumerate(PP):
        puzz_save = deepcopy(puzz)
        s.set_grid(puzz)

        t0 = time.perf_counter()
        res = solve(s)
        t1 = time.perf_counter()

        print(Sudoku().set_grid(puzz_save))
        print("")
        print(res)
        print(f"-----{t1 - t0:.3f}s-------")
        print()

        ts.append(t1 - t0)

        if i % 1000 == 0:
            print(f"{i} / {len(PP)} = {i / len(PP):.3f}")
