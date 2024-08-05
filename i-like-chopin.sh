#!/bin/sh
if ! hash python3; then
    echo "python3 is not installed"
    exit 1
fi
cd src/
poetry run python i-like-chopin.py
