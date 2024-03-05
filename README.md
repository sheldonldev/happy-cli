# README

Commonly used commands for myself. It should use together with VSCode.

## Usage

```bash
# see help
jam -h
```

## Development

```sh
pip install -e ".[dev]"

# if local dependencies updated, please update the wheels.
# this script will read the target dependencies' pyproject.toml
# to copy the .whl file under the ./wheel, as whell as 
# update the ./install_wheels.sh script, automatically.
python scripts/update_wheels.py

# run this bash to install wheels
bash install_wheels.sh
```

## Build Package

```sh
python -m pip install --upgrade build
python -m build
```
