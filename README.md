# Distributed-systems

## How to run
Start the service by running:
```
    docker compose up
```

## "Kanban"

TODO:
- [] fix

## Dev environment

### Setup

```
python3.12 -m venv --clear .venv
source .venv/bin/activate
pip install --editable main_node[dev] --editable chat_node[dev] --editable client[dev]
```

### Linting, formatting, type checking, import sorting

```
black  --check --config black.toml . &&
isort --check-only --settings isort.toml . &&
pylint --rcfile pylintrc.toml --recursive=y --ignore=.venv .  &&
mypy --config-file mypy.toml .
```
