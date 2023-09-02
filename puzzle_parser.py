#! /usr/bin/env python3

"""
Parse puzzles from the Sudoku forum database. They are in the form of
12...4.5..... etc for 81 characters, row major.
"""

import numpy as np

from pathlib import Path


DEFAULT_PUZZLES = Path(__file__).parent / "puzzles" / "ph_2010" / "02_index.txt"


class PuzzleParser:
    def __init__(self, puzzle_path: Path = DEFAULT_PUZZLES) -> None:
        """
        3,103,972 puzzles are ~277 MB, so just load them into memory
        """
        with open(puzzle_path, "r") as f:
            raw_puzzle_string = f.read()
            np_puzzles = PuzzleParser._process_raw_puzzles(raw_puzzle_string)

        self._puzzles = np_puzzles

    def __getitem__(self, idx: int) -> np.ndarray:
        return self._puzzles[idx]

    def __len__(self) -> int:
        return self._puzzles.shape[0]

    @staticmethod
    def _process_raw_puzzles(puzzles_string: str) -> np.ndarray:
        puzzles_by_line = puzzles_string.strip().split("\n")

        # filter out indexes
        puzzles_by_line = [puzz.split(";")[0] for puzz in puzzles_by_line]

        # process into something that we can make into a np array
        preprocessed_puzzles = [
            [0 if c == "." else int(c) for c in puzzle_string]
            for puzzle_string in puzzles_by_line
        ]

        np_puzzles = np.asarray(preprocessed_puzzles, dtype=np.uint8)
        np_puzzles = np_puzzles.reshape(-1, 9, 9)
        return np_puzzles


if __name__ == "__main__":
    p = PuzzleParser()
