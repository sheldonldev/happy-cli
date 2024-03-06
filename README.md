# README

Commonly used commands for myself. It should use together with VSCode.

## Usage

```bash
# see help
jam -h
```

## Development

### Step 1: Install the Package Edetably

```sh
pip install -e ".[dev]"
```

### Step2 : Install

- There are two methods to install dependent wheels.

- Method 1:

```sh
# if local dependencies updated, please update the wheels.
# this script will read the target dependencies' pyproject.toml
# to copy the .whl file under the ./wheel, as whell as 
# update the ./install_wheels.sh script, automatically.
python scripts/update_wheels.py

# run this bash to install wheels
bash install_wheels.sh
```

- Method 2:

```sh
pip install -e ~/repos/jampy_util/jampy_util
```

## Build Package

```sh
python -m pip install --upgrade build
python -m build
```
