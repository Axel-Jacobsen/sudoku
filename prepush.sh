#! /usr/bin/env bash

ruff . --fix
echo "__"
mypy .

echo "__"
black .

echo "__"

python3 -m unittest discover .
echo "__"

python3 performance_test.py --n-iters 20
