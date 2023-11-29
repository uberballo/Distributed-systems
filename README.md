# Distributed-systems

## How to run
Start the service by running:
```
    docker compose up
```

## "Kanban"

TODO:
- [ ] Send messages to a chat node
- [ ] Get messages from a chat node
- [ ] Get neighbors from the main node
- [ ] Implement proper initialization to a chat node
- [ ] Ping main node when a new chat nodes joins
- [ ] Add health checker to main node
- [ ] Create a client that communicates with a chat node

## Dev environment

### Setup

```
python3.12 -m venv --clear .venv
source .venv/bin/activate
pip install --editable main_node[dev] --editable chat_node[dev] --editable client[dev]
```

### Linting, formatting, type checking, import sorting

After activating the environment and installing applications and dependencies: `make check`
