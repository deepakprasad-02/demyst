#!/bin/sh

if [ "$1" = "test" ]; then
    pytest -v
elif [ "$1" = "main" ]; then
    python src/sol_one/main.py
else
    echo "Invalid argument. Use 'test' to run pytest or 'main' to run main.py"
    exit 1
fi