#!/bin/bash
pip install -e ".[dev]"
pip install -e "../jampy_util_common"
pre-commit install
mypy --install-types
