#!/bin/bash
pip install -e "../jampy_util_common"
pip install -e ".[dev]"

pre-commit install
mypy --install-types
