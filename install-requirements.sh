#!/bin/bash
set -e

if [ ! -d ".venv" ]; then
    python3 -m venv .venv
    echo "Virtual environment '.venv' created"
fi

source .venv/bin/activate
echo "Requirements:"
cat requirements.txt
echo
pip install --upgrade pip
pip install -r requirements.txt
echo "Requirements installed successfully in '.venv'"

