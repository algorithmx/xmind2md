#!/bin/bash

python3 -m venv .env

source .env/bin/activate

echo 'click==7.1.2' > requirements.txt