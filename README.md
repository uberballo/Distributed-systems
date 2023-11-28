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

After activating the environment and installing applications and dependencies: `make check`
