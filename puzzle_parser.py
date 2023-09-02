#! /usr/bin/env python3

"""
Parse puzzles from the Sudoku forum database. They are in the form of
12...4.5..... etc for 81 characters, row major.
"""

import time
import numpy as np

from pathlib import Path
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
            np_puzzles = PuzzleParser._process_raw_puzzles(raw_puzzle_string)

        self._puzzles = np_puzzles
        self._idx: Optional[int] = None

    def __getitem__(self, idx: int) -> List[List[Optional[int]]]:
        return self._puzzles[idx].tolist()

    def __len__(self) -> int:
        return self._puzzles.shape[0]

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
    def _process_raw_puzzles(puzzles_string: str) -> np.ndarray:
        puzzles_by_line = puzzles_string.strip().split("\n")

        # filter out indexes
        puzzles_by_line = [puzz.split(";")[0] for puzz in puzzles_by_line]

        # process into something that we can make into a np array
        preprocessed_puzzles = [
            [None if c == "." else int(c) for c in puzzle_string]
            for puzzle_string in puzzles_by_line
        ]

        np_puzzles = np.asarray(preprocessed_puzzles)
        np_puzzles = np_puzzles.reshape(-1, 9, 9)
        return np_puzzles


if __name__ == "__main__":
    print("loading puzzles...")
    PP = PuzzleParser()
    print(f"loaded {len(PP)} puzzles")

    ts: List[float] = []
    s = Sudoku()

    for i, puzz in enumerate(PP):
        s.set_grid(puzz)

        t0 = time.perf_counter()
        solve(s)
        t1 = time.perf_counter()

        ts.append(t1 - t0)

        if i % 1000 == 0:
            print(f"{i} / {len(PP)} = {i / len(PP):.3f}")
