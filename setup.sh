#!/usr/bin/env bash

python3 -m venv .venv
python -m pip install --upgrade pip

source "./.venv/bin/activate"

pip install -r requirements.txt

cp ".env_example" ".env"

printf "%s\n" "Activate virtual env with source .venv/bin/activate"