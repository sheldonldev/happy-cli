#!/bin/bash
python scripts/update_wheels.py
pip install --find-links="./wheels" jampy_util
pip install --find-links="./wheels" jampy_util_intelligence