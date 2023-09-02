#! /usr/bin/env bash

echo "__"
black .

ruff . --fix
echo "__"
mypy .

echo "__"
echo "(second black call to clean up after ruff fix)"
black . --quiet

echo "__"

python3 -m unittest discover .
echo "__"

python3 performance_test.py --n-iters 32
