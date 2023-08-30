#! /usr/bin/env bash

ruff . --fix
mypy .
black .
python3 -m unittest discover .
