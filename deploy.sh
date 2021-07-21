#!/bin/bash

# update version in setup.cfg by hand.

set -euxo pipefail
rm -f dist/*
pytest
python setup.py sdist
pip install twine
twine upload dist/*

