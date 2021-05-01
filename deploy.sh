#!/bin/bash
set -euxo pipefail
rm -f dist/*
pytest
python setup.py sdist
pip install twine
twine upload dist/*

