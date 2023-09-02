#! /usr/bin/env python3

import time

from sudoku import Sudoku


def test_performance_solve_1(N=16):
    assert N > 0

    s = Sudoku(
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
    truth = Sudoku(
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

    ts = []
    for i in range(N):
        t0 = time.perf_counter()
        solved = s.solve()
        assert solved == truth, "sudoku not solved correctly in performance test"
        t1 = time.perf_counter()
        ts.append(t1 - t0)
        s._board.set_grid(
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

    mean_time = sum(ts) / len(ts)
    print(f"mean solve duration {mean_time:.5f} seconds")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--n-iters", type=int, default=16)
    args = parser.parse_args()

    test_performance_solve_1(args.n_iters)
